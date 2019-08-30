#
# RTEMS Project (https://www.rtems.org/)
#
# Copyright (c) 2019 Vijay Kumar Banerjee <vijaykumar9597@gmail.com>.
# All rights reserved.
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

import shlex
import os
import re
import rtems_waf.rtems as rtems

def source_list():
    mk_files = ['lvgl/src/lv_core/lv_core.mk',
                'lvgl/src/lv_hal/lv_hal.mk',
                'lvgl/src/lv_objx/lv_objx.mk',
                'lvgl/src/lv_font/lv_font.mk',
                'lvgl/src/lv_misc/lv_misc.mk',
                'lvgl/src/lv_themes/lv_themes.mk',
                'lvgl/src/lv_draw/lv_draw.mk',
                'lv_drivers/display/display.mk']
    sources = []
    cflags = []

    for filename in mk_files:
      lexer = shlex.shlex(file(filename, 'rt').read())
      lexer.whitespace += '+='
      lexer.whitespace_split = True

      for token in lexer:
          if token == 'CSRCS':
              source_path = os.path.dirname(filename)
              source_path = os.path.join(source_path, next(lexer))
              sources.append(source_path)

          if token == 'CFLAGS':
              cflag = next(lexer)
              if(cflag[14] == '/'):
                  cflags.append(cflag[15:-1])
              else:
                  cflags.append(cflag[14:-1])

    return (sources, cflags)

def build(bld):

    sources, includes = source_list()
    includes.append('.')
    objects = []
    include_paths = []

    for source in sources:
        objects.append(source[:-1] + 'o')
        source_dir = os.path.dirname(source)
        if source_dir not in include_paths:
            include_paths.append(source_dir)

    bld.objects(target = objects,
                features = 'c',
                cflags = '-O2',
                includes = includes,
                source = source)

    bld.stlib(target = 'lvgl',
              features = 'c',
              includes = includes,
              source = sources,
              use = objects)

    arch_lib_path = rtems.arch_bsp_lib_path(bld.env.RTEMS_VERSION,
                                            bld.env.RTEMS_ARCH_BSP)
    arch_inc_path = rtems.arch_bsp_include_path(bld.env.RTEMS_VERSION,
                                                bld.env.RTEMS_ARCH_BSP)

    include_paths.extend(['lvgl/', 'lv_drivers', 'lvgl/src', '.'])
    for include_path in include_paths:
        files = os.listdir(include_path)
        include_headers = [os.path.join(include_path, x) for x in files if (x[-2:] == '.h')]
        bld.install_files(os.path.join("${PREFIX}/" , arch_inc_path, include_path),
                          include_headers)
    bld.install_files('${PREFIX}/' + arch_lib_path, ["liblvgl.a"])
