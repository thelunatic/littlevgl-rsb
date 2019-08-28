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


def source_list():
    mk_files = ['lvgl/src/lv_core/lv_core.mk',
                'lvgl/src/lv_hal/lv_hal.mk',
                'lvgl/src/lv_objx/lv_objx.mk',
                'lvgl/src/lv_font/lv_font.mk',
                'lvgl/src/lv_misc/lv_misc.mk',
                'lvgl/src/lv_themes/lv_themes.mk',
                'lvgl/src/lv_draw/lv_draw.mk',]
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
              sources.append(os.path.abspath(source_path))

          if token == 'CFLAGS':
              cflag = next(lexer).replace('$(LVGL_DIR)', str(os.getcwd()))
              cflags.append(cflag)
    return (sources, cflags)
