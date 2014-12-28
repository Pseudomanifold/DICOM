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

def formatFilename(prefix,
                   width, height, depth,
                   bits, unsigned):
  """
  Generates a filename using a prefix and the base parameters of all images.
  """

  return format("%s_%dx%dx%d_%d%s") % (prefix,
                                       width, height, depth,
                                       bits, "u" if unsigned == 0 else "s" )


def getParameters(filename):
  """
  Reads the relevant parameters (width, height, and so on) of a single file. No
  direct error handling is performed.
  """

  f = dicom.read_file(filename)

  return f.PatientsName,\
         f.Columns,\
         f.Rows,\
         f.BitsAllocated,\
         f.PixelRepresentation

def isValid(filename, name, width, height, bits, unsigned):
  """
  Checks whether a given DICOM file is valid and refers to the same patient.
  """

  f = dicom.read_file(filename)

  return     f.PatientsName        == name\
         and f.Columns             == width\
         and f.Rows                == height\
         and f.BitsAllocated       == bits\
         and f.PixelRepresentation == unsigned

def checkFiles(filenames):
  """
  Checks and prunes a list of filenames. Only those filenames that refer to the
  same patient and whose pixel data have the same dimensions will be returned.
  for furher processing.
  """

  if not filenames:
    raise Exception("List of filenames must not be empty")

  name, width, height, bits, unsigned = getParameters(filenames[0])

  return [ filename for filename in filenames if isValid(filename,
                                                         name,
                                                         width, height, bits, unsigned) ]

#
# main
#

parser = argparse.ArgumentParser(description="This program concatenates pixel data of DICOM files. All files need to have the same image dimensions and refer to the same patient for the concatenation to work.")
parser.add_argument("files", metavar="FILE", type=str, nargs="+", help="File for concatenation")
parser.add_argument("--prefix", help="Prefix for output file")
parser.add_argument("--check", action="store_true", help="Check files prior to conversion")

arguments = parser.parse_args()

name     = None
width    = None
height   = None
bits     = None
unsigned = None
outFile  = sys.stdout

if arguments.check:
  filenames = checkFiles(arguments.files)
else:
  filenames = arguments.files

for index,filename in enumerate(filenames):
  f = dicom.read_file(filename) 

  percentage = 100.0 * (index+1) / float(len(filenames))

  print("[%6.2f%%] Processing '%s'..." % (percentage, os.path.basename(filename) ),
        file=sys.stderr)

  if index == 0:
    name     = f.PatientsName
    width    = f.Columns
    height   = f.Rows
    bits     = f.BitsAllocated
    unsigned = f.PixelRepresentation

    # Open output file for writing if necessary
    if arguments.prefix:
      outFile = open(formatFilename(arguments.prefix,
                                    width, height, len(arguments.files),
                                    bits, unsigned), "w")
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

  outFile.write( f.PixelData )
