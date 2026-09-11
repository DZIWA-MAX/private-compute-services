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

# Shim for Google's internal mirror of kotlinx.coroutines.
#
# The internal tree splits the library by platform variant; the public
# Maven coordinates below are the same artifacts JetBrains publishes.
# Pinned at 1.6.4, the last release built against the Kotlin 1.7 compiler
# that rules_kotlin 1.7.1 registers (KOTLIN_CURRENT_COMPILER_RELEASE =
# 1.7.22); coroutines 1.7+ require Kotlin 1.8.20 or newer.

package(default_visibility = ["//visibility:public"])

# org.jetbrains.kotlinx:kotlinx-coroutines-android
# Adds the Android main-thread dispatcher on top of the core artifact.
alias(
    name = "kotlinx_coroutines-android",
    actual = "@maven//:org_jetbrains_kotlinx_kotlinx_coroutines_android",
)

# org.jetbrains.kotlinx:kotlinx-coroutines-core-jvm
# The JVM variant of the multiplatform `kotlinx-coroutines-core` artifact.
# rules_jvm_external resolves plain Maven metadata, not Gradle module
# metadata, so the `-jvm` coordinate has to be named explicitly.
alias(
    name = "kotlinx_coroutines-jvm",
    actual = "@maven//:org_jetbrains_kotlinx_kotlinx_coroutines_core_jvm",
)

# org.jetbrains.kotlinx:kotlinx-coroutines-guava
# Published as a single JVM artifact; both internal variants map onto it.
alias(
    name = "kotlinx_coroutines_guava-android",
    actual = "@maven//:org_jetbrains_kotlinx_kotlinx_coroutines_guava",
)

alias(
    name = "kotlinx_coroutines_guava-jvm",
    actual = "@maven//:org_jetbrains_kotlinx_kotlinx_coroutines_guava",
)
