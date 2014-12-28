#!/usr/bin/env python2
#
# recursive_conversion --- Concatenates and converts a directory tree recursively
#
# This script is useful for concatenating multiple series of DICOM files from
# e.g. multiple runs of an MRI machine. Assuming that different DICOM series
# are stored in subdirectories of the form Data/2011/STUD01/SER??, you could
# call the script as follows:
#
#   ./recursive_conversion.py Data/2011/STUD01
#
# The result will be a series of files that are named SER??_x_y_z_b[u|s], where
# x, y, and z refer to the dimensions of the concatenated raw DICOM volume, b
# contains the number of bits for representing a single entry, and u|s
# indicates whether data is (un)signed.
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

import os
import subprocess
import sys

for directory, subdirectories, files in os.walk(sys.argv[1], topdown=False):
  if files:
    prefix    = os.path.basename(directory)
    filenames = [ str(os.path.join(directory, x)) for x in files ]

    subprocess.call(["./dicomcat.py", "--check", "--prefix", prefix ] + filenames)
