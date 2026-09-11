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

# Shim for Google's internal mirror of gRPC Java.
#
# All coordinates are pinned at 1.51.1 to match the io.grpc artifacts
# already listed in WORKSPACE.

package(default_visibility = ["//visibility:public"])

# io.grpc:grpc-okhttp
# There is no separate "-android" artifact upstream: grpc-okhttp is the
# transport gRPC recommends on Android, and the internal target name only
# reflects which dependency set Google's build strips for Android.
alias(
    name = "okhttp_android",
    actual = "@maven//:io_grpc_grpc_okhttp",
)

# io.grpc:grpc-cronet
alias(
    name = "cronet_api_android",
    actual = "@maven//:io_grpc_grpc_cronet",
)

# io.grpc:grpc-core
alias(
    name = "core",
    actual = "@maven//:io_grpc_grpc_core",
)

# io.grpc:grpc-stub
alias(
    name = "stub",
    actual = "@maven//:io_grpc_grpc_stub",
)
