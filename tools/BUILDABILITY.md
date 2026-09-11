# Buildability of this export

This repository is a Copybara mirror of Google-internal code. `CONTRIBUTING`
states that it exists to let developers read the implementation, and that is
what it supports: the export omits Google-internal `.bzl` helpers, several
`third_party` packages, and two external repositories, so most of the tree
cannot be built as published.

Run `python3 tools/buildability_map.py` to reproduce the numbers below, and
`--list` / `--blocked` for the per-target detail.

## Current state

| | targets |
|---|---|
| total | 698 |
| buildable | 152 (22%) |
| blocked | 546 |

`build.sh` ends with `bazel build //src/com/google/android/as/oss:pcs`. That
target does not exist. `src/com/google/android/as/oss/BUILD` defines `release`
via the `pcs_dev_and_mpm` macro, loaded from
`//src/com/google/android/as/oss:build_defs.bzl`, which is not in the export.
The APK cannot be produced here.

## Root cause of the 546 blocked targets

| cause | targets |
|---|---|
| `load()` of an unexported `.bzl` | 294 |
| dependency on an unexported package | 110 |
| blocked transitively | 101 |
| symbol not exported by the pinned `rules_android` | 37 |
| undeclared external repository | 3 |
| dependency on a package broken by its own loads | 1 |

### Largest remaining blockers

`//third_party/protobuf/build_defs:kt_jvm_proto_library.bzl` alone accounts for
218 targets. It must supply `kt_jvm_lite_proto_library` (39 call sites) and
`kt_jvm_proto_library` (2). Unlike the four rules shimmed in
`third_party/protobuf/bazel`, these have no native Bazel 6 equivalent, and the
protobuf version pulled in transitively by `rules_proto_grpc` 4.0.1 predates
protobuf's own Kotlin Bazel rules. A faithful shim needs a custom rule invoking
`protoc --kotlin_out`; forwarding to `java_lite_proto_library` instead would
build, but would emit Java bindings and break any Kotlin source using the
generated proto DSL.

Ten packages load `kt_jvm_library_with_nullness_check` or
`java_library_with_nullness_check` from `@bazel_rules_android//android:rules.bzl`.
The pinned `v0.1.1` tag exports neither — those names are internal to Google —
and an absent symbol fails the whole `BUILD` file, not just the one target.

`@federated_compute` and `@private_retrieval` are referenced by `BUILD` files
but never declared in `WORKSPACE`, so federated compute cannot be built even
though the README points at its open-source repository.

The unexported package dependencies are mostly Google's internal mirrors of
public libraries — `//third_party/java/androidx/compose/*`,
`//third_party/kotlin/kotlinx_coroutines`, `//third_party/java/androidx/appsearch`,
`//third_party/oak/*`. Each would need a `BUILD` shim pointing at the
corresponding `@maven` artifact.

## What the proto shims recovered

Adding `third_party/protobuf/bazel` moved the count from 131 to 152 with no
regression. The 21 recovered targets are the proto and gRPC API layers:

- `asr/api` (9) — the SRSG speech proxy service and its feature config
- `attestation/api` (2), `http/api` (2), `pir/api` (2), `survey/api` (2)
- `pd/persistence` (2) and `pd/virtualmachine/impl` (1)
- `protos` (1) — the PCS feature enum

## Caveat

This is static analysis, not a verified build. `glob()` in `srcs` is not
expanded and implicitly generated targets are not modelled, so the buildable
count is an optimistic upper bound. Nothing here has been confirmed by running
Bazel.

## Note on running the app

Building a subset of targets does not produce a usable app.
`src/com/google/android/as/oss/AndroidManifest.xml` declares
`minSdkVersion="36"` and requests signature- and privileged-level permissions
(`PROVIDE_PRIVATE_COMPUTE_SERVICES`, `WRITE_SECURE_SETTINGS`,
`READ_RESTRICTED_STATS`, `MANAGE_VIRTUAL_MACHINE`), which the platform grants
only to system-partition apps signed with the platform key. Its
`<allow-component-access>` block further pins the certificate digests of the
Google first-party apps it talks to.
