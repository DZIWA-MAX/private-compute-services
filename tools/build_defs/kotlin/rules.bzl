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

"""Kotlin gRPC rules for this repository.

The BUILD files here load `kt_jvm_grpc_library` from this label because that is
where it lives in Google's internal source tree. Upstream grpc-kotlin ships the
same macro with a matching signature -- name, srcs, deps and a flavor of
"normal" or "lite" -- so this re-exports it rather than reimplementing the
protoc-gen-grpc-kotlin plumbing. WORKSPACE declares the repository.

Starlark does not re-export loaded symbols, hence the rebinding below.
"""

load(
    "@com_github_grpc_grpc_kotlin//:kt_jvm_grpc.bzl",
    _kt_jvm_grpc_library = "kt_jvm_grpc_library",
)

kt_jvm_grpc_library = _kt_jvm_grpc_library
