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

"""Kotlin protobuf rules for this repository.

The BUILD files here load `kt_jvm_lite_proto_library` and `kt_jvm_proto_library`
from this label because that is where they live in Google's internal source
tree. Unlike the rules shimmed in //third_party/protobuf/bazel, Bazel 6 has no
native equivalent, and the protobuf release pinned transitively through
rules_proto_grpc 4.0.1 (v3.18.0) predates protobuf's own Kotlin Bazel rules.

So these are implemented here. protoc's Kotlin generator emits a DSL that sits
on top of the generated Java classes rather than replacing them, so each macro
expands to three targets: the Kotlin sources from protoc, the matching Java
proto library, and a kt_jvm_library tying them together and exporting the Java
classes so that dependents see both.

Depending on the same proto_library from both a java_lite_proto_library here
and one declared directly in a BUILD file does not duplicate classes: Bazel
implements those rules with an aspect over proto_library, so the generated
output is shared.
"""

load("@io_bazel_rules_kotlin//kotlin:jvm.bzl", "kt_jvm_library")

# Path separator for --descriptor_set_in. build.sh only supports Linux, and
# use_bazel.sh rejects anything but Linux and macOS, so ":" always holds.
_PATH_SEPARATOR = ":"

def _import_path(source, proto_source_root):
    """Maps a .proto file to the name it carries inside the descriptor set."""
    path = source.path
    if proto_source_root in ("", "."):
        return path
    if path.startswith(proto_source_root + "/"):
        return path[len(proto_source_root) + 1:]
    return path

def _kotlin_proto_srcjar_impl(ctx):
    proto_infos = [dep[ProtoInfo] for dep in ctx.attr.deps]

    # protoc decides between a directory and an archive by looking at the
    # output suffix, and it only recognises .jar and .zip. Kotlin rules only
    # accept .srcjar in srcs, so generate the .jar and symlink it across.
    jar = ctx.actions.declare_file(ctx.label.name + ".jar")
    srcjar = ctx.actions.declare_file(ctx.label.name + ".srcjar")

    descriptor_sets = depset(
        transitive = [info.transitive_descriptor_sets for info in proto_infos],
    )

    args = ctx.actions.args()
    args.add_joined(
        "--descriptor_set_in",
        descriptor_sets,
        join_with = _PATH_SEPARATOR,
    )
    args.add("--kotlin_out", jar, format = "lite:%s" if ctx.attr.lite else "%s")
    for info in proto_infos:
        for source in info.direct_sources:
            args.add(_import_path(source, info.proto_source_root))

    ctx.actions.run(
        executable = ctx.executable._protoc,
        arguments = [args],
        inputs = descriptor_sets,
        outputs = [jar],
        mnemonic = "KotlinProtoGen",
        progress_message = "Generating Kotlin protos for %{label}",
    )
    ctx.actions.symlink(output = srcjar, target_file = jar)
    return [DefaultInfo(files = depset([srcjar]))]

_kotlin_proto_srcjar = rule(
    implementation = _kotlin_proto_srcjar_impl,
    doc = "Runs protoc's Kotlin generator over deps and returns a .srcjar.",
    attrs = {
        "deps": attr.label_list(
            providers = [ProtoInfo],
            mandatory = True,
            doc = "proto_library targets to generate Kotlin bindings for.",
        ),
        "lite": attr.bool(
            default = True,
            doc = "Generate against protobuf-lite rather than the full runtime.",
        ),
        "_protoc": attr.label(
            default = Label("@com_google_protobuf//:protoc"),
            executable = True,
            cfg = "exec",
        ),
    },
)

def _kt_proto_library(name, deps, lite, runtime, **kwargs):
    srcjar = name + "_kt_srcjar"
    java = name + "_java"

    _kotlin_proto_srcjar(
        name = srcjar,
        deps = deps,
        lite = lite,
        visibility = ["//visibility:private"],
    )
    if lite:
        native.java_lite_proto_library(name = java, deps = deps)
    else:
        native.java_proto_library(name = java, deps = deps)

    kt_jvm_library(
        name = name,
        srcs = [":" + srcjar],
        deps = [":" + java, runtime],
        exports = [":" + java],
        **kwargs
    )

def kt_jvm_lite_proto_library(name, deps, **kwargs):
    """Kotlin bindings against protobuf-lite, the variant used on Android."""
    _kt_proto_library(
        name = name,
        deps = deps,
        lite = True,
        runtime = "@maven//:com_google_protobuf_protobuf_kotlin_lite",
        **kwargs
    )

def kt_jvm_proto_library(name, deps, **kwargs):
    """Kotlin bindings against the full protobuf runtime."""
    _kt_proto_library(
        name = name,
        deps = deps,
        lite = False,
        runtime = "@maven//:com_google_protobuf_protobuf_kotlin",
        **kwargs
    )
