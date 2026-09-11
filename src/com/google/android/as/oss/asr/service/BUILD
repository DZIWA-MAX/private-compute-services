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

load("@bazel_rules_android//android:rules.bzl", "android_library")

package(default_visibility = [
    "//src/com/google/android/as/oss:__subpackages__",
])

android_library(
    name = "service",
    srcs = [
        "SrsgProxyServiceHelper.java",
        "SrsgProxyServiceImpl.java",
        "SrsgProxyServiceModule.java",
    ],
    deps = [
        "//src/com/google/android/as/oss/common/security/api:package_security_info_java_proto_lite",
        "//src/com/google/android/as/oss/common/security/config",
        "@maven//:androidx_annotation_annotation",
        "@maven//:androidx_lifecycle_lifecycle_service",
        "//src/com/google/android/as/oss/common/config",
        "//src/com/google/android/as/oss/asr/config",
        "//src/com/google/android/as/oss/asr/config/impl",
        "//src/com/google/android/as/oss/asr/api:srsg_proxy_java_grpc_lite",
        "//src/com/google/android/as/oss/asr/api:srsg_proxy_java_proto_lite",
        "//src/com/google/android/as/oss/common/security:security_policy_utils",
        "//src/com/google/android/as/oss/grpc:annotations",
        "//java/com/google/android/libraries/speech/transcription/recognition/grpc:google_asr_service_parcelables",
        "//java/com/google/frameworks/client/data/android/binder:google_security_policies",
        "//java/com/google/frameworks/client/data/android/server/contrib/parcelables:client_interceptor",
        # Dagger/Hilt
        "//java/com/google/android/libraries/concurrent:prod_hilt_module",
        "@maven//:com_google_dagger_dagger",
        "@maven//:com_google_dagger_hilt_android",
        # gRPC
        "//java/com/google/frameworks/client/data/android/server/contrib/parcelables",
        "@maven//:io_grpc_grpc_binder",
        "@maven//:io_grpc_grpc_api",
        "@maven//:io_grpc_grpc_stub",
        "@maven//:io_grpc_grpc_context",
        # Other
        "@maven//:com_google_guava_guava",
        "@maven//:com_google_flogger_google_extensions",
        "@maven//:com_google_code_findbugs_jsr305",
        "@maven//:javax_inject_javax_inject",
    ],
)
