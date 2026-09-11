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

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Pull down rules_jvm_external for integrateing external dependencies
RULES_JVM_EXTERNAL_TAG = "4.5"

RULES_JVM_EXTERNAL_SHA = "b17d7388feb9bfa7f2fa09031b32707df529f26c91ab9e5d909eb1676badd9a6"

http_archive(
    name = "rules_jvm_external",
    sha256 = RULES_JVM_EXTERNAL_SHA,
    strip_prefix = "rules_jvm_external-%s" % RULES_JVM_EXTERNAL_TAG,
    url = "https://github.com/bazelbuild/rules_jvm_external/archive/%s.zip" % RULES_JVM_EXTERNAL_TAG,
)

# Load dagger/hilt repository
DAGGER_TAG = "2.44.2"

DAGGER_SHA = "cbff42063bfce78a08871d5a329476eb38c96af9cf20d21f8b412fee76296181"

http_archive(
    name = "dagger",
    sha256 = DAGGER_SHA,
    strip_prefix = "dagger-dagger-%s" % DAGGER_TAG,
    urls = ["https://github.com/google/dagger/archive/dagger-%s.zip" % DAGGER_TAG],
)

# grpc-kotlin supplies kt_jvm_grpc_library, which //tools/build_defs/kotlin
# re-exports. Declared here because the maven_install below needs its
# artifacts. git_repository rather than http_archive because this environment
# cannot fetch the release archive to compute a sha256; pin one when possible.
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "com_github_grpc_grpc_kotlin",
    remote = "https://github.com/grpc/grpc-kotlin.git",
    tag = "v1.3.0",
)

load(
    "@com_github_grpc_grpc_kotlin//:repositories.bzl",
    "IO_GRPC_GRPC_KOTLIN_ARTIFACTS",
    "IO_GRPC_GRPC_KOTLIN_OVERRIDE_TARGETS",
    "grpc_kt_repositories",
)
load(
    "@dagger//:workspace_defs.bzl",
    "HILT_ANDROID_ARTIFACTS",
    "HILT_ANDROID_REPOSITORIES",
)
load("@rules_jvm_external//:repositories.bzl", "rules_jvm_external_deps")

rules_jvm_external_deps()

load("@rules_jvm_external//:setup.bzl", "rules_jvm_external_setup")

rules_jvm_external_setup()

load("@rules_jvm_external//:defs.bzl", "maven_install")

maven_install(
    artifacts = HILT_ANDROID_ARTIFACTS + IO_GRPC_GRPC_KOTLIN_ARTIFACTS + [
        "com.google.auto.value:auto-value:1.10.1",
        "com.google.auto.value:auto-value-annotations:1.10.1",
        "com.ryanharter.auto.value:auto-value-parcel:0.2.9",
        "com.ryanharter.auto.value:auto-value-parcel-adapter:0.2.9",
        "com.google.dagger:dagger:2.44.2",
        "javax.inject:javax.inject:1",
        "com.google.guava:guava:31.1-android",
        "androidx.annotation:annotation:1.5.0",
        "androidx.lifecycle:lifecycle-service:2.5.1",
        "androidx.lifecycle:lifecycle-livedata:2.5.1",
        "androidx.preference:preference:1.2.0",
        "androidx.fragment:fragment:1.5.1",
        "androidx.fragment:fragment-ktx:1.5.1",
        "androidx.swiperefreshlayout:swiperefreshlayout:1.1.0",
        "androidx.activity:activity:1.6.1",
        "androidx.activity:activity-ktx:1.6.1",
        "com.google.errorprone:error_prone_annotations:2.17.0",
        "androidx.core:core:1.9.0",
        "androidx.room:room-runtime:2.4.3",
        # Backing artifacts for the //third_party/java/androidx shims. Versions
        # track the Compose 2022.10.00 BOM (Compose 1.3.0, Material3 1.0.0),
        # co-released with the activity 1.6.1, lifecycle 2.5.1 and core 1.9.0
        # already pinned above. rules_jvm_external 4.5 cannot consume a BOM, so
        # every coordinate is listed explicitly.
        "androidx.activity:activity-compose:1.6.1",
        "androidx.appcompat:appcompat:1.6.1",
        # AppSearch has no stable release; this alpha is unverified against the
        # SearchSpec and SetSchemaRequest usage in src/.
        "androidx.appsearch:appsearch:1.0.0-alpha03",
        "androidx.compose.animation:animation-core:1.3.0",
        "androidx.compose.animation:animation:1.3.0",
        "androidx.compose.foundation:foundation-layout:1.3.0",
        "androidx.compose.foundation:foundation:1.3.0",
        "androidx.compose.material3:material3:1.0.0",
        "androidx.compose.runtime:runtime:1.3.0",
        "androidx.compose.ui:ui-graphics:1.3.0",
        "androidx.compose.ui:ui-unit:1.3.0",
        "androidx.compose.ui:ui:1.3.0",
        "androidx.core:core-ktx:1.9.0",
        "androidx.datastore:datastore-core:1.0.0",
        "androidx.hilt:hilt-navigation-compose:1.0.0",
        # 2.8.x folds work-runtime-ktx into work-runtime, which the sources need
        # for CoroutineWorker; an alias carries a single target, so the split
        # artifact of 2.7.x and earlier would not work here.
        "androidx.work:work-runtime:2.8.1",
        # Backing artifact for the //third_party/java/android_libs shims.
        # 1.7.0 is the Material release that lines up with the androidx
        # versions pinned here.
        "com.google.android.material:material:1.7.0",
        # Backing artifacts for the //third_party/kotlin shims. Kotlin is
        # 1.7.22, the compiler release rules_kotlin 1.7.1 registers, and
        # coroutines 1.6.4 is the last line built against that compiler:
        # 1.7 and newer need Kotlin 1.8.20.
        "org.jetbrains.kotlin:kotlin-parcelize-runtime:1.7.22",
        "org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4",
        "org.jetbrains.kotlinx:kotlinx-coroutines-core-jvm:1.6.4",
        "org.jetbrains.kotlinx:kotlinx-coroutines-guava:1.6.4",
        "androidx.lifecycle:lifecycle-livedata-core:2.5.1",
        "com.google.api.grpc:proto-google-common-protos:2.12.0",
        "io.grpc:grpc-protobuf-lite:1.51.1",
        "io.grpc:grpc-netty-shaded:1.51.1",
        "io.grpc:grpc-binder:1.51.1",
        "io.grpc:grpc-core:1.51.1",
        "io.grpc:grpc-stub:1.51.1",
        "io.grpc:grpc-context:1.51.1",
        # Backing artifacts for the //third_party/java/grpc shims, at the same
        # 1.51.1 as the rest of io.grpc above.
        "io.grpc:grpc-cronet:1.51.1",
        "io.grpc:grpc-okhttp:1.51.1",
        "com.google.protobuf:protobuf-lite:3.0.1",
        # Runtime for the Kotlin DSL that protoc generates on top of the
        # Java classes. Pinned to the protobuf version that
        # rules_proto_grpc 4.0.1 supplies, so protoc and runtime agree.
        "com.google.protobuf:protobuf-kotlin:3.18.0",
        "com.google.protobuf:protobuf-kotlin-lite:3.18.0",
        "com.squareup.okhttp3:okhttp:4.10.0",
        "com.google.flogger:google-extensions:0.7.4",
    ],
    fetch_sources = True,
    override_targets = IO_GRPC_GRPC_KOTLIN_OVERRIDE_TARGETS,
    repositories = HILT_ANDROID_REPOSITORIES + [
        "https://jcenter.bintray.com/",
        "https://maven.google.com",
        "https://repo1.maven.org/maven2",
        "https://plugins.gradle.org/m2/",
    ],
)

# Pull down rules to generate a Java protobuf and gRPC library using java_library
http_archive(
    name = "rules_proto_grpc",
    sha256 = "28724736b7ff49a48cb4b2b8cfa373f89edfcb9e8e492a8d5ab60aa3459314c8",
    strip_prefix = "rules_proto_grpc-4.0.1",
    urls = ["https://github.com/rules-proto-grpc/rules_proto_grpc/archive/4.0.1.tar.gz"],
)

load("@rules_proto_grpc//:repositories.bzl", "rules_proto_grpc_repos", "rules_proto_grpc_toolchains")

rules_proto_grpc_toolchains()

rules_proto_grpc_repos()

load("@rules_proto_grpc//java:repositories.bzl", rules_proto_grpc_java_repos = "java_repos")

rules_proto_grpc_java_repos()

load("@io_grpc_grpc_java//:repositories.bzl", "IO_GRPC_GRPC_JAVA_ARTIFACTS", "IO_GRPC_GRPC_JAVA_OVERRIDE_TARGETS", "grpc_java_repositories")

maven_install(
    name = "java_grpc",
    artifacts = IO_GRPC_GRPC_JAVA_ARTIFACTS,
    generate_compat_repositories = True,
    override_targets = IO_GRPC_GRPC_JAVA_OVERRIDE_TARGETS,
    repositories = [
        "https://repo.maven.apache.org/maven2/",
    ],
)

load("@java_grpc//:compat.bzl", "compat_repositories")

compat_repositories()

grpc_java_repositories()

android_sdk_repository(
    name = "androidsdk",
    api_level = 33,
)

# Allows us to use android_library and android_binary rules.
http_archive(
    name = "bazel_rules_android",
    sha256 = "cd06d15dd8bb59926e4d65f9003bfc20f9da4b2519985c27e190cddc8b7a7806",
    strip_prefix = "rules_android-0.1.1",
    urls = ["https://github.com/bazelbuild/rules_android/archive/v0.1.1.zip"],
)

# Allow dependency on policy_java_proto_lite from private compute libraries.
RULES_KOTLIN_VERSION = "1.7.1"

RULES_KOTLIN_SHA = "fd92a98bd8a8f0e1cdcb490b93f5acef1f1727ed992571232d33de42395ca9b3"

# Allows us to use kt_android_library, kt_jvm_library, and friends.
http_archive(
    name = "io_bazel_rules_kotlin",
    sha256 = RULES_KOTLIN_SHA,
    urls = ["https://github.com/bazelbuild/rules_kotlin/releases/download/v%s/rules_kotlin_release.tgz" % RULES_KOTLIN_VERSION],
)

load("@io_bazel_rules_kotlin//kotlin:repositories.bzl", "kotlin_repositories")

kotlin_repositories()

load("@io_bazel_rules_kotlin//kotlin:core.bzl", "kt_register_toolchains")

kt_register_toolchains()

# No-ops for io_bazel_rules_kotlin, com_google_protobuf and io_grpc_grpc_java,
# which are all declared above: in WORKSPACE the first declaration of a
# repository wins, so the versions pinned here are the ones that apply.
grpc_kt_repositories()

git_repository(
    name = "private_compute_libraries",
    remote = "https://github.com/google/private-compute-libraries.git",
    tag = "v0.1.0-20230105",
)

# The README names federated compute as an open-source dependency, but no
# repository was ever declared for it, so every //src/com/google/android/as/oss/fl
# target referencing @federated_compute//fcp/client:fl_runner fails to resolve.
# That target is public and, at this revision, does not require TensorFlow: the
# BUILD file gates //fcp/client/engine:plan_engine behind a support_tfmobile
# flag that is off by default.
#
# Pinned by commit because the repository publishes no tags.
#
# Not declared alongside it: @private_retrieval. The README names it too, and
# two targets here reference @private_retrieval//private_retrieval/java:pir and
# //private_retrieval/java/core, but google/private-retrieval ships the 28 Java
# sources with no BUILD file anywhere under private_retrieval/java -- only the
# cpp tree is buildable. Declaring the repository would not make either label
# resolve.
git_repository(
    name = "federated_compute",
    commit = "4f4895971dddb6b0631f2cf31464e39bcc71186c",
    remote = "https://github.com/google/federated-compute.git",
)
