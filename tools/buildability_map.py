#!/usr/bin/env python3
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Reports which Bazel targets in this export can still be built.

This repository is a Copybara mirror of Google-internal code, so many BUILD
files load .bzl helpers or depend on packages that were never exported. This
script parses every BUILD file, resolves each label against what is actually on
disk and against the repositories declared in WORKSPACE, then propagates the
failures transitively to find the targets that remain buildable.

It is a static approximation, not a build: glob() in srcs is not expanded and
implicitly generated targets are not modelled, so treat the result as an
optimistic upper bound.

Usage:  python3 tools/buildability_map.py [--list] [--blocked]
"""

import argparse
import collections
import os
import re
import signal
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# External repositories declared in WORKSPACE, plus the ones Bazel provides.
DECLARED_REPOS = frozenset([
    "androidsdk", "bazel_rules_android", "bazel_tools", "com_google_protobuf",
    "dagger", "io_bazel_rules_kotlin", "io_grpc_grpc_java", "java_grpc",
    "maven", "platforms", "private_compute_libraries", "rules_cc", "rules_java",
    "rules_jvm_external", "rules_proto", "rules_proto_grpc", "rules_python",
])

# Symbols @bazel_rules_android//android:rules.bzl actually exports at the tag
# pinned in WORKSPACE (v0.1.1). Loading anything else fails the whole BUILD file.
RULES_ANDROID_SYMBOLS = frozenset([
    "RULES_ANDROID_VERSION", "aar_import", "android_binary", "android_device",
    "android_instrumentation_test", "android_library", "android_local_test",
    "android_ndk_repository", "android_sdk_repository",
])

# Attributes whose labels are not dependencies.
NON_DEP_ATTRS = re.compile(
    r"\b(visibility|default_visibility|compatible_with|applicable_licenses"
    r"|restricted_to|tags|features)\s*=\s*(\[[^\]]*\]|[A-Za-z_0-9.\"]+)", re.S)

LOAD_RE = re.compile(r'load\(\s*"([^"]+)"([^)]*)\)', re.S)
CALL_START_RE = re.compile(r"^([a-zA-Z_][a-zA-Z_0-9]*)\(", re.M)
NAME_RE = re.compile(r'\bname\s*=\s*"([^"]+)"')
LABEL_RE = re.compile(r'"(@?[A-Za-z0-9_./:@+~-]*(?://|:)[A-Za-z0-9_./:@+~-]*)"')
SYMBOL_RE = re.compile(r'"([a-zA-Z_][a-zA-Z_0-9]*)"')

NOT_A_RULE = frozenset(["load", "package", "licenses", "exports_files",
                        "package_group"])


def find_build_files():
    for base in ("src", "third_party"):
        for dirpath, _, filenames in os.walk(os.path.join(ROOT, base)):
            for name in filenames:
                if name in ("BUILD", "BUILD.bazel"):
                    yield os.path.join(dirpath, name)


def iter_calls(text):
    """Yields (rule, body) for each top-level call, tracking nested parens.

    A regex cannot do this: a one-line call such as package(...) would otherwise
    run to the closing paren of the next rule block and swallow it.
    """
    for match in CALL_START_RE.finditer(text):
        depth = 0
        quote = None
        index = match.end() - 1
        while index < len(text):
            char = text[index]
            if quote:
                if char == "\\":
                    index += 2
                    continue
                if char == quote:
                    quote = None
            elif char in "\"'":
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    yield match.group(1), text[match.end():index]
                    break
            index += 1


def parse_package(build_file):
    """Returns (missing_loads, bad_symbol, targets) for one BUILD file."""
    text = open(build_file, encoding="utf-8", errors="replace").read()
    text = "\n".join(re.sub(r"#.*$", "", line) for line in text.split("\n"))

    missing_loads = []
    bad_symbol = None
    for match in LOAD_RE.finditer(text):
        label, args = match.group(1), match.group(2)
        if label.startswith("//"):
            pkg, _, bzl = label[2:].partition(":")
            if not os.path.isfile(os.path.join(ROOT, pkg, bzl)):
                missing_loads.append(label)
        elif label.startswith("@"):
            repo = label[1:].split("//")[0]
            if repo and repo not in DECLARED_REPOS:
                missing_loads.append(label)
            elif label == "@bazel_rules_android//android:rules.bzl":
                for symbol in SYMBOL_RE.findall(args):
                    if symbol not in RULES_ANDROID_SYMBOLS and not bad_symbol:
                        bad_symbol = symbol

    targets = {}
    for rule, body in iter_calls(text):
        if rule in NOT_A_RULE:
            continue
        name = NAME_RE.search(body)
        if not name:
            continue
        body = NON_DEP_ATTRS.sub("", body)
        labels = {m.group(1) for m in LABEL_RE.finditer(body)
                  if m.group(1).startswith(("//", "@", ":"))}
        targets[name.group(1)] = {"rule": rule, "labels": sorted(labels)}

    return sorted(set(missing_loads)), bad_symbol, targets


def resolve(label, current_package):
    """Maps a label to ('repo', name) or ('target', 'pkg:name'), or None."""
    if label.startswith("@"):
        return ("repo", label[1:].split("//")[0])
    if label.startswith(":"):
        return ("target", current_package + ":" + label[1:])
    if label.startswith("//"):
        pkg, sep, name = label[2:].partition(":")
        if not sep:
            name = pkg.rsplit("/", 1)[-1]
        return ("target", pkg + ":" + name)
    return None


def analyze():
    packages = {}
    for build_file in find_build_files():
        pkg = os.path.relpath(os.path.dirname(build_file), ROOT)
        missing, bad_symbol, targets = parse_package(build_file)
        packages[pkg] = {"missing_loads": missing, "bad_symbol": bad_symbol,
                         "targets": targets}

    known = {pkg + ":" + name
             for pkg, data in packages.items() for name in data["targets"]}

    blocked = {}
    edges = {}
    for pkg, data in packages.items():
        for name, target in data["targets"].items():
            key = pkg + ":" + name
            if data["missing_loads"]:
                blocked[key] = ("missing load", data["missing_loads"][0])
            elif data["bad_symbol"]:
                blocked[key] = ("unexported symbol",
                                data["bad_symbol"] + " @bazel_rules_android")
            deps = set()
            for label in target["labels"]:
                resolved = resolve(label, pkg)
                if not resolved:
                    continue
                kind, value = resolved
                if kind == "repo":
                    if value not in DECLARED_REPOS:
                        blocked.setdefault(key, ("undeclared repo", "@" + value))
                elif value in known:
                    deps.add(value)
                else:
                    dep_pkg = value.split(":")[0]
                    if dep_pkg in packages:
                        if packages[dep_pkg]["missing_loads"]:
                            blocked.setdefault(
                                key, ("broken package", "//" + dep_pkg))
                    else:
                        blocked.setdefault(key, ("missing dep", "//" + value))
            edges[key] = deps

    changed = True
    while changed:
        changed = False
        for key, deps in edges.items():
            if key in blocked:
                continue
            for dep in deps:
                if dep in blocked:
                    blocked[key] = ("transitive", "//" + dep)
                    changed = True
                    break

    return packages, sorted(known - set(blocked)), blocked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true",
                        help="print every buildable target")
    parser.add_argument("--blocked", action="store_true",
                        help="print the root cause for every blocked target")
    args = parser.parse_args()

    packages, buildable, blocked = analyze()
    total = len(buildable) + len(blocked)

    print("BUILD files : %d" % len(packages))
    print("targets     : %d" % total)
    print("buildable   : %d (%.0f%%)" % (len(buildable),
                                         100.0 * len(buildable) / total))
    print("blocked     : %d" % len(blocked))

    print("\nroot cause of blocked targets")
    causes = collections.Counter(cause for cause, _ in blocked.values())
    for cause, count in causes.most_common():
        print("  %5d  %s" % (count, cause))

    print("\nbuildable targets by module")
    by_module = collections.Counter()
    for key in buildable:
        pkg = key.split(":")[0]
        if pkg.startswith("src/com/google/android/as/oss/"):
            module = pkg[len("src/com/google/android/as/oss/"):].split("/")[0]
        else:
            module = pkg
        by_module[module] += 1
    for module, count in by_module.most_common():
        print("  %5d  %s" % (count, module))

    if args.list:
        print("\nbuildable targets")
        for key in buildable:
            print("  //" + key)

    if args.blocked:
        print("\nblocked targets")
        for key in sorted(blocked):
            cause, detail = blocked[key]
            print("  //%s  [%s: %s]" % (key, cause, detail))

    return 0


if __name__ == "__main__":
    # Let the process die quietly when piped into a short-lived reader (head).
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
