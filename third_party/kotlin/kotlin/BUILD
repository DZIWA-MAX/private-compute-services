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

# Shim for Google's internal mirror of the Kotlin runtime libraries.
#
# Pinned at 1.7.22, the Kotlin release that rules_kotlin 1.7.1 registers
# (KOTLIN_CURRENT_COMPILER_RELEASE in its versions.bzl), so the runtime
# matches the compiler that builds against it.

package(default_visibility = ["//visibility:public"])

# org.jetbrains.kotlin:kotlin-parcelize-runtime
# Supplies the `kotlinx.parcelize.Parcelize` annotation and the
# `Parceler` helpers. Note that the annotation only carries meaning when
# the Kotlin `parcelize` compiler plugin runs; rules_kotlin 1.7.1 has no
# attribute for enabling it, so sources using @Parcelize still need that
# plugin wired up before they will actually produce a CREATOR.
alias(
    name = "parcelize_runtime",
    actual = "@maven//:org_jetbrains_kotlin_kotlin_parcelize_runtime",
)
