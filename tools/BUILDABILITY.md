# Buildability of this export

This repository is a Copybara mirror of Google-internal code. `CONTRIBUTING`
states that it exists to let developers read the implementation, and that is
what it supports: the export omits Google-internal `.bzl` helpers, many
`third_party` packages, and several external repositories.

Run `python3 tools/buildability_map.py` to reproduce the numbers, `--list` and
`--blocked` for per-target detail, and `--maven` to audit `@maven` labels.

## Current state

| | targets |
|---|---|
| total | 931 |
| buildable | 432 (46%) |
| blocked | 499 |

Starting point was 131. What moved it, in order:

| change | buildable |
|---|---|
| as exported | 131 |
| `third_party/protobuf/bazel` shims for the native proto rules | 152 |
| `kt_jvm_proto_library` / `kt_jvm_lite_proto_library` | 238 |
| `kt_jvm_grpc_library` re-exported from grpc-kotlin | ~269 |
| `third_party/java/androidx` shims | ~310 |
| `third_party/kotlin`, `java/grpc`, `android_libs`, `dagger/hilt` shims | 432 |

Counts before and after a parser fix are not comparable: the map used to let a
one-line `package(...)` call swallow the rule following it, so totals below 916
are undercounts against a denominator of 698.

`build.sh` ends with `bazel build //src/com/google/android/as/oss:pcs`. That
target does not exist. `src/com/google/android/as/oss/BUILD` defines `release`
via the `pcs_dev_and_mpm` macro, loaded from
`//src/com/google/android/as/oss:build_defs.bzl`, which is not in the export.
The APK cannot be produced here.

## Root cause of the 499 blocked targets

| cause | targets |
|---|---|
| blocked transitively | 205 |
| dependency on an unexported package | 132 |
| `load()` of an unexported `.bzl` | 85 |
| symbol not exported by the pinned `rules_android` | 70 |
| undeclared external repository | 7 |

### Remaining blockers

Ten packages load `kt_jvm_library_with_nullness_check` or
`java_library_with_nullness_check` from `@bazel_rules_android//android:rules.bzl`.
The pinned `v0.1.1` exports neither — they are internal to Google — and an
absent symbol fails the whole `BUILD` file, not just one target. Fixing this
means patching the external repository or editing those loads.

`@federated_compute`, `@private_retrieval` and Project Oak are referenced but
never declared in `WORKSPACE`. Recovering them needs new repository rules and a
Bazel path to their Java clients, not aliases.

Several dependencies cannot be shimmed at all, because no public artifact
corresponds to them:

- `//third_party/java/android_libs/safeparcel` — the federated-compute fork of
  SafeParcelable, published nowhere; its annotation processor likewise.
- `//third_party/java/android_libs/settingslib` — AOSP SettingsLib, compiled
  inside the platform tree.
- `//third_party/java/protobuf:java_features_proto` and
  `//third_party/protobuf:cpp_features_proto` — `proto_library` targets for
  protobuf Editions, which postdate the 3.18.0 resolved here. These are
  consumed through an `option_deps` attribute that Bazel 6's native
  `proto_library` does not have, so the shim in `third_party/protobuf/bazel`
  will reject those call sites even once the label resolves.
- `//java/com/google/...`, `//google/internal/...`, `//googledata/...`,
  `//third_party/java/android/android_sdk_linux/...` — Google-internal, never
  published.

## Caveats

Nothing here has been built. Bazel is not installed in the environment this was
produced in, and the egress proxy blocks Maven Central archives and Google
Maven, so no POM was fetched and no version co-resolution was exercised. What
is verified is static label resolution, plus upstream source reads for the
protoc flags, the `rules_android` and grpc-kotlin exports, and
rules_jvm_external's name mangling.

The map is an optimistic upper bound for a further reason: `glob()` in `srcs`
is not expanded, implicitly generated targets are not modelled, and a label
pointing at a missing target inside a package that does exist is treated as
resolvable.

Three known gaps in what the shims provide, all of which will surface only at
compile time:

- `alias` has no `exported_plugins`, so the Room, AppSearch and Compose
  annotation processors are unwired.
- `kotlin-parcelize-runtime` supplies the `@Parcelize` annotation, but
  rules_kotlin 1.7.1 exposes no way to enable the parcelize compiler plugin, so
  no `CREATOR` is generated.
- The `androidx.appsearch` coordinate is an alpha, since AppSearch has no
  stable release, and is unverified against the API the sources use.

## Note on running the app

Building a subset of targets does not produce a usable app.
`src/com/google/android/as/oss/AndroidManifest.xml` declares
`minSdkVersion="36"` and requests signature- and privileged-level permissions
(`PROVIDE_PRIVATE_COMPUTE_SERVICES`, `WRITE_SECURE_SETTINGS`,
`READ_RESTRICTED_STATS`, `MANAGE_VIRTUAL_MACHINE`), which the platform grants
only to system-partition apps signed with the platform key. Its
`<allow-component-access>` block further pins the certificate digests of the
Google first-party apps it talks to.
