
# vim: set foldmethod=marker fmr=\#—,\#\# :

#:::::::::::::::::::::::::::::::::::::::: embed-lut.py

# Tucks a .cube LUT inside a preview PNG, so one picture carries both: what a
# color map looks like, and the map itself. The pixels and every other chunk
# are copied across untouched; the cube goes into one more text chunk (iTXt,
# keyword "phase-lut"), zlib-compressed, word for word. Viewers that don't
# know the chunk ignore it.
#
# Re-saving the result in Photoshop will most likely drop the chunk: edit the
# PSD and run this again instead.
#
# usage:
#   python3 -I embed-lut.py preview.png map.cube [out.png]
#
# writes out.png (default: preview.lut.png beside the preview) and prints the
# cube's SHA-256, a fingerprint for checking a copy against the original
# (`shasum -a 256 map.cube` gives the same number).
#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2026 Andrew C. Swift
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import hashlib
import os
import struct
import sys
import zlib

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
KEYWORD = b'phase-lut'

#:::::::::::::::::::::::::::::::::::::::: functionality

def main():
  if len(sys.argv) not in (3, 4):
    sys.exit('usage: embed-lut.py preview.png map.cube [out.png]')
  preview, cube = sys.argv[1], sys.argv[2]
  out = sys.argv[3] if len(sys.argv) == 4 else os.path.splitext(preview)[0] + '.lut.png'
  join_png_and_cube(preview, cube, out)

#:::::::::::::::::::::::::::::::::::::::: main functions

#———————————————————————————————————————— join_png_and_cube(preview, cube, out)

#   copies the preview's chunks to out, with the cube's chunk just before IEND;
#   an older phase-lut chunk in the preview is left out, so running it twice
#   doesn't stack two cubes

def join_png_and_cube(preview, cube, out):
  with open(preview, 'rb') as f:
    png = f.read()
  with open(cube, 'rb') as f:
    cube_text = f.read()
  check_cube(cube_text)

  chunks = read_chunks(png)
  lut_chunk = make_chunk(b'iTXt', itxt_data(KEYWORD, cube_text))
  written = []
  with open(out, 'wb') as f:
    f.write(PNG_SIGNATURE)
    for kind, data in chunks:
      if kind == b'iTXt' and data.split(b'\x00', 1)[0] == KEYWORD:
        continue
      if kind == b'IEND':
        f.write(lut_chunk)
        written.append('iTXt phase-lut')
      f.write(make_chunk(kind, data))
      written.append(kind.decode('latin-1'))

  print(f'wrote {out}')
  print(f'  chunks: {" ".join(c for c in written if c != "IDAT")} (+ {written.count("IDAT")} IDAT)')
  print(f'  cube: {len(cube_text):,} bytes, {len(lut_chunk):,} in the PNG')
  print(f'  cube sha256: {hashlib.sha256(cube_text).hexdigest()}')
##

#:::::::::::::::::::::::::::::::::::::::: worker functions

#———————————————————————————————————————— read_chunks(png)

#   the PNG as a list of (kind, data), checking each chunk's CRC on the way

def read_chunks(png):
  if not png.startswith(PNG_SIGNATURE):
    sys.exit('not a PNG')
  chunks, i = [], len(PNG_SIGNATURE)
  while i < len(png):
    length, kind = struct.unpack('>I4s', png[i:i + 8])
    data = png[i + 8:i + 8 + length]
    crc, = struct.unpack('>I', png[i + 8 + length:i + 12 + length])
    if zlib.crc32(kind + data) != crc:
      sys.exit(f'bad CRC in {kind.decode("latin-1")} chunk')
    chunks.append((kind, data))
    i += 12 + length
    if kind == b'IEND':
      break
  return chunks
##
#———————————————————————————————————————— make_chunk(kind, data)

#   length, kind, data, CRC of kind + data

def make_chunk(kind, data):
  return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
##
#———————————————————————————————————————— itxt_data(keyword, text)

#   an iTXt chunk's data: keyword, compressed (flag 1, method 0), no language,
#   no translated keyword, then the text zlib-compressed

def itxt_data(keyword, text):
  return keyword + b'\x00' + b'\x01\x00' + b'\x00' + b'\x00' + zlib.compress(text, 9)
##
#———————————————————————————————————————— check_cube(text)

#   refuses anything that isn't a 3D .cube with the right number of rows

def check_cube(text):
  size, rows = None, 0
  for line in text.decode('utf-8', 'replace').splitlines():
    line = line.strip()
    if line.startswith('LUT_3D_SIZE'):
      size = int(line.split()[1])
    elif line and (line[0].isdigit() or line[0] in '-.'):
      rows += 1
  if size is None:
    sys.exit('no LUT_3D_SIZE line: not a 3D .cube')
  if rows != size ** 3:
    sys.exit(f'LUT_3D_SIZE {size} needs {size ** 3} rows, found {rows}')
##

# Python needs the functions defined before it can run them, so the call that
# starts it all sits here rather than under "functionality". The guard runs it
# only when the file is run as a script, not when it's imported.
if __name__ == '__main__':
  main()

#:::::::::::::::::::::::::::::::::::::::: fin

