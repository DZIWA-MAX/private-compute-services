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

"""Shim exposing Bazel's native `cc_library` rule.

Google's internal tree mirrors the public Bazel rules under
//third_party/bazel_rules, and the BUILD files here load from those paths.
Bazel 6 still provides this rule natively, so the shim forwards to it. Wrapping
is required because `native` is not accessible at the top level of a .bzl file.
"""

def cc_library(**kwargs):
    native.cc_library(**kwargs)
