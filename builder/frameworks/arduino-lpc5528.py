# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduino-lpc5528")
assert isdir(FRAMEWORK_DIR)
SYSTEM_DIR = join(FRAMEWORK_DIR, "system")
USB_DIR = join(SYSTEM_DIR, "CMSIS","lib","usb")
FATFS_DIR = join(SYSTEM_DIR, "CMSIS","lib","fatfs")

# USB flags
ARDUINO_USBDEFINES = [
    "ARDUINO_ARCH_LPC5528",
    ("ARDUINOLPC", 10805)
]

env.Append(
    CPPDEFINES=ARDUINO_USBDEFINES,

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", env.BoardConfig().get("build.core"))
    ],

    LINKFLAGS=[
        "-Wl,-T" + join(SYSTEM_DIR, "CMSIS/system/LPC55S28_flash.ld") + ",--gc-sections,--relax",
    ]
)

#
# CMSIS
#

env.Append(
    CPPPATH=[
        join(SYSTEM_DIR, "CMSIS", "include"),
        join(SYSTEM_DIR, "CMSIS", "system"),
        join(SYSTEM_DIR, "CMSIS", "lib"),
        join(USB_DIR),
        join(USB_DIR,"device"),
        join(USB_DIR,"device","class"),
        join(USB_DIR,"device","class","cdc"),
        join(USB_DIR,"device","include"),
        join(USB_DIR,"device","source"),
        join(USB_DIR,"device","source","lpcip3511"),
        join(USB_DIR,"host"),
        join(USB_DIR,"host","class"),
        join(USB_DIR,"include"),
        join(USB_DIR,"phy"),
        join(FATFS_DIR),
        join(FATFS_DIR,"source"),
        join(FATFS_DIR,"source","fsl_ram_disk"),
        join(FATFS_DIR,"source","fsl_usb_disk")
    ],

    LIBPATH=[
        join(SYSTEM_DIR, "CMSIS", "bin")
    ],

    LIBS=["power_softabi"]
)

#
# lpc176x interface
#

env.Append(
    CPPPATH=[
        join(SYSTEM_DIR, "lpc5528"),
    ],

    LIBS=[]
)

#
# Lookup for specific core's libraries
#

BOARD_CORELIBDIRNAME = env.BoardConfig().get("build.core", "")
env.Append(
    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries", "__cores__", BOARD_CORELIBDIRNAME),
        join(FRAMEWORK_DIR, "libraries")
    ]
)

#
# Target: Build Core Library
#

libs = []

libs.append(env.BuildLibrary(
                join("$BUILD_DIR", "CMSIS"),
                join(FRAMEWORK_DIR, "system", "CMSIS")
))

libs.append(env.BuildLibrary(
                join("$BUILD_DIR", "lpc5528"),
                join(FRAMEWORK_DIR, "system", "lpc5528")
))

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants",
                 env.BoardConfig().get("build.variant"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.variant"))
    ))

libs.append(env.BuildLibrary(
                join("$BUILD_DIR", "FrameworkArduino"),
                join(FRAMEWORK_DIR, "cores", env.BoardConfig().get("build.core"))            
))

env.Prepend(LIBS=libs)
