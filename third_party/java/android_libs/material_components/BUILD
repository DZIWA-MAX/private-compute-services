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

# Shim for Google's internal mirror of Material Components for Android.
#
# The internal tree has one target per component; upstream publishes the
# whole library as a single AAR, com.google.android.material:material, so
# every component target maps onto it. Pinned at 1.7.0, the release that
# lines up with the androidx versions in WORKSPACE (core 1.9.0,
# fragment 1.5.1, activity 1.6.1, lifecycle 2.5.1).

package(default_visibility = ["//visibility:public"])

# com.google.android.material.dialog.MaterialAlertDialogBuilder
alias(
    name = "dialog",
    actual = "@maven//:com_google_android_material_material",
)

# com.google.android.material.chip.Chip
alias(
    name = "chip",
    actual = "@maven//:com_google_android_material_material",
)

# com.google.android.material.materialswitch.MaterialSwitch
alias(
    name = "materialswitch",
    actual = "@maven//:com_google_android_material_material",
)
