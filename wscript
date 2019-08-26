#
# RTEMS Project (https://www.rtems.org/)
#
# Copyright (c) 2019 Vijay Kumar Banerjee. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#
# TODO: This file is a work in progress and isn't supposed to run yet.
#

from __future__ import print_function

rtems_version = "5"

try:
    import rtems_waf.rtems as rtems
except:
    print("error: no rtems_waf git submodule; see README.waf")
    import sys
    sys.exit(1)

import os.path
import runpy
import sys
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import waflib.Options

builders = {}

def bsp_init(ctx, env, contexts):
    # This function generates the builders and adds build-xxx, clean-xxx and
    # install-xxx targets for them.

    # Transform the commands to per build variant commands
    commands = []
    for cmd in waflib.Options.commands:
        if cmd.startswith(('build', 'clean', 'install')):
            for builder in builders:
                commands += [cmd + '-' + builder]
        else:
            commands += [cmd]
    waflib.Options.commands = commands

def init(ctx):
    rtems.init(ctx, version = rtems_version, long_commands = True,
               bsp_init = bsp_init)

def options(opt):
    rtems.options(opt)
    opt.add_option("--enable-warnings",
                   action = "store_true",
                   default = False,
                   dest = "warnings",
                   help = "Enable all warnings. The default is quiet builds.")

def bsp_configure(conf, arch_bsp):
    env = conf.env.derive()

def configure(conf):
    conf.env.WARNINGS = conf.options.warnings

    rtems.configure(conf, bsp_configure)

def build(bld):
    rtems.build(bld)
