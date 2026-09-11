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

# Shim for Google's internal mirror of Hilt.
#
# The internal tree exposes one target per annotation surface. Upstream
# ships a single hilt-android artifact, and this repository already wires
# it up together with every Hilt annotation processor in
# //third_party/java/hilt, via dagger's own hilt_android_rules() macro.
# These aliases forward there rather than to a bare @maven jar: the Hilt
# annotations are inert without the processors that target attaches.

package(default_visibility = ["//visibility:public"])

# dagger.hilt.EntryPoint / dagger.hilt.EntryPoints, plus the
# hilt_aggregated_deps and hilt_root processors that generate their
# implementations.
alias(
    name = "entry_point",
    actual = "//third_party/java/hilt:hilt-android",
)

# dagger.hilt.android.HiltAndroidApp
alias(
    name = "hilt_android_app",
    actual = "//third_party/java/hilt:hilt-android",
)

# dagger.hilt.android.lifecycle.HiltViewModel
alias(
    name = "view_model",
    actual = "//third_party/java/hilt:hilt-android",
)
