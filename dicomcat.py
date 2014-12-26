#!/usr/bin/env python2
#
# dicomcat --- Concatenates the raw data of a bunch of DICOM images
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

import argparse
import dicom
import os
import sys

parser = argparse.ArgumentParser(description="This program concatenates pixel data of DICOM files. All files need to have the same image dimensions and refer to the same patient for the concatenation to work.")
parser.add_argument("files", metavar="FILE", type=str, nargs="+", help="File for concatenation")

arguments = parser.parse_args()

name     = None
width    = None
height   = None
bits     = None
unsigned = None

for index,filename in enumerate(arguments.files):
  f = dicom.read_file(filename) 
  if index == 0:
    name     = f.PatientsName
    width    = f.Columns
    height   = f.Rows
    bits     = f.BitsAllocated
    unsigned = f.PixelRepresentation
  else:
    if f.PatientsName != name:
      raise Exception("Name must agree over all files")
    if f.Columns != width:
      raise Exception("Width must agree over all files")
    if f.Rows != height:
      raise Exception("Height must agree over all files")
    if f.BitsAllocated != bits:
      raise Exception("Number of bits must agree over all files")
    if f.PixelRepresentation != unsigned:
      raise Exception("Representation (signed/unsigned) must agree over all files")

  percentage = 100.0 * index / float(len(arguments.files)-1)

  print("[%6.2f%%] Processing '%s'..." % (percentage, os.path.basename(filename) ),
        file=sys.stderr)

  sys.stdout.write( f.PixelData )
