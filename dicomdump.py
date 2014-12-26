#!/usr/bin/env python2
#
# dicomdump --- Dumps DICOM raw image data
#
# The purpose of this tool is to open a DICOM file and dump its pixel data
# contents to STDOUT, while showing some informative statistics about the file
# on STDERR. This program does not make any assumptions about the internal
# structure of the DICOM file. Neither will it attempt to transform the pixel
# data in any way.
#
# Copyright (c) 2014 Bastian Rieck 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import dicom
import sys

def usage():
  print("Usage: dicomdump FILE", file=sys.stderr)

if len(sys.argv) != 2:
  usage()
  sys.exit(-1)

f              = dicom.read_file( sys.argv[1] )
bits           = f.BitsAllocated
width          = f.Columns
height         = f.Rows
representation = f.PixelRepresentation
interpretation = f.PhotometricInterpretation
samples        = f.SamplesPerPixel

# pydicom is lazy and reports the raw bytes in the `PixelData` section exactly
# as they are found. There is no reason why we should not do the same. The
# burden is thus on the user to obtain a usable RAW file.

sys.stdout.write( f.PixelData )

#
# Header (or rather the footer)
#

print("##############\n"
      "# Pixel data #\n"
      "##############\n\n"
      "Width:                      %d\n"
      "Height:                     %d\n"
      "Samples:                    %d\n"
      "Bits:                       %d\n"
      "Photometric interpretation: %s\n"
      "Unsigned:                   %d\n"
        % (width, height, samples, bits, interpretation, representation == 0 ),
      file=sys.stderr)
