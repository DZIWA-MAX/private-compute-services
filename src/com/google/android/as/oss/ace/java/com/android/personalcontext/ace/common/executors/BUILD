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

package(
    default_visibility = [
        "//third_party/java/android_app/personalcontext:libraries",
    ],
)

android_library(
    name = "safe_main_thread_executor",
    srcs = [
        "SafeMainThreadExecutor.kt",
    ],
    deps = [
        "@maven//:javax_inject_javax_inject",
    ],
)

android_library(
    name = "safe_main_thread_executor_module",
    srcs = [
        "SafeMainThreadExecutorModule.kt",
    ],
    deps = [
        ":safe_main_thread_executor",
        "@maven//:com_google_dagger_dagger",
        "@maven//:com_google_dagger_hilt_android",
    ],
)
