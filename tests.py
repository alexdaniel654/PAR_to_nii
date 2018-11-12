# -*- coding: utf-8 -*-
"""
Created: 08/11/2018
Last update: 12/11/2018
Alex Daniel, Sir Peter Mansfield Imaging Centre, The University of Nottingham, 2018.

Tests for pton
"""

import unittest
import subprocess
import nibabel as nib
import numpy as np
import glob
import os


def run_pton(in_file, flags=''):
    cmd = 'python pton.py .\\test_data\\' + in_file + ' ' + flags
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def same_data(test_file, gold_file):
    test_img = nib.load('.\\test_data\\' + test_file)
    test_data = test_img.get_data()
    gold_img = nib.load('.\\test_data\\gold_data\\' + gold_file)
    gold_data = gold_img.get_data()
    return np.allclose(test_data, gold_data)


class TestAngio(unittest.TestCase):

    def test_full_vol(self):
        run_pton('angio.PAR')
        self.assertTrue(same_data('angio.nii.gz', 'gold_angio.nii.gz'))

    def tearDown(self):
        files = glob.glob('.\\test_data\\angio*.nii.gz')
        [os.remove(f) for f in files]


if __name__ == '__main__':
    unittest.main()
