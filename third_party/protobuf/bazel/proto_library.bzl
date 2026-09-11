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

"""Shim exposing Bazel's native `proto_library` rule.

The BUILD files in this repository load `proto_library` from this label because
that is where it lives in Google's internal source tree. Bazel 6 still provides
the rule natively, so the shim only has to forward to it. Wrapping is required
because the `native` module is not accessible at the top level of a .bzl file.

Generates descriptors from .proto sources for the language-specific proto rules to consume.
"""

def proto_library(**kwargs):
    native.proto_library(**kwargs)
