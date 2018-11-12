# -*- coding: utf-8 -*-
"""
Created: 08/11/2018
Last update: 09/11/2018
Alex Daniel, Sir Peter Mansfield Imaging Centre, The University of Nottingham, 2018.

Removes all the converted files from the test data folder i.e. gets rid of the .nii.gz outputs from pton
"""

import os
import glob

files = glob.glob('./test_data/*.nii.gz')

for file in files:
    print('Removing ' + file)
    os.remove(file)
