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
    cmd = 'python pton.py ./test_data/' + in_file + ' ' + flags
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    process.communicate()


def same_data(test_file, gold_file):
    test_img = nib.load('./test_data/' + test_file)
    test_data = test_img.get_data()
    gold_img = nib.load('./test_data/gold_data/' + gold_file)
    gold_data = gold_img.get_data()
    return np.allclose(test_data, gold_data)


class TestType(unittest.TestCase):

    def test_full_vol(self):
        run_pton('image_type_mr.PAR')
        self.assertTrue(same_data('image_type_mr.nii.gz', 'gold_image_type_mr.nii.gz'))

    def test_type(self):
        run_pton('image_type_mr.PAR', '-t')
        self.assertTrue(same_data('image_type_mr_real.nii.gz', 'gold_image_type_mr_real.nii.gz'))
        self.assertTrue(same_data('image_type_mr_imag.nii.gz', 'gold_image_type_mr_imag.nii.gz'))
        self.assertTrue(same_data('image_type_mr_mag.nii.gz', 'gold_image_type_mr_mag.nii.gz'))
        self.assertTrue(same_data('image_type_mr_phase.nii.gz', 'gold_image_type_mr_phase.nii.gz'))

    def tearDown(self):
        files = glob.glob('./test_data/image_type_mr*.nii.gz')
        [os.remove(f) for f in files]


class TestAngio(unittest.TestCase):

    def test_full_vol(self):
        run_pton('angio.PAR')
        self.assertTrue(same_data('angio.nii.gz', 'gold_angio.nii.gz'))

    def test_phase(self):
        run_pton('angio.PAR', '-p')
        self.assertTrue(same_data('angio_phase_1.nii.gz', 'gold_angio_phase_1.nii.gz'))
        self.assertTrue(same_data('angio_phase_5.nii.gz', 'gold_angio_phase_5.nii.gz'))
        self.assertTrue(same_data('angio_phase_10.nii.gz', 'gold_angio_phase_10.nii.gz'))
        self.assertTrue(same_data('angio_phase_15.nii.gz', 'gold_angio_phase_15.nii.gz'))

    def test_type(self):
        run_pton('angio.PAR', '-t')
        self.assertTrue(same_data('angio_mag.nii.gz', 'gold_angio_mag.nii.gz'))
        self.assertTrue(same_data('angio_phase.nii.gz', 'gold_angio_phase.nii.gz'))

    def test_phase_type(self):
        run_pton('angio.PAR', '-pt')
        self.assertTrue(same_data('angio_phase_1_phase.nii.gz', 'gold_angio_phase_1_phase.nii.gz'))
        self.assertTrue(same_data('angio_phase_5_phase.nii.gz', 'gold_angio_phase_5_phase.nii.gz'))
        self.assertTrue(same_data('angio_phase_10_phase.nii.gz', 'gold_angio_phase_10_phase.nii.gz'))
        self.assertTrue(same_data('angio_phase_15_phase.nii.gz', 'gold_angio_phase_15_phase.nii.gz'))
        self.assertTrue(same_data('angio_phase_1_mag.nii.gz', 'gold_angio_phase_1_mag.nii.gz'))
        self.assertTrue(same_data('angio_phase_5_mag.nii.gz', 'gold_angio_phase_5_mag.nii.gz'))
        self.assertTrue(same_data('angio_phase_10_mag.nii.gz', 'gold_angio_phase_10_mag.nii.gz'))
        self.assertTrue(same_data('angio_phase_15_mag.nii.gz', 'gold_angio_phase_15_mag.nii.gz'))

    def tearDown(self):
        files = glob.glob('./test_data/angio*.nii.gz')
        [os.remove(f) for f in files]


class TestASL(unittest.TestCase):

    def test_full_vol(self):
        run_pton('asl.PAR')
        self.assertTrue(same_data('asl.nii.gz', 'gold_asl.nii.gz'))

    def test_label(self):
        run_pton('asl.PAR', '-l')
        self.assertTrue(same_data('asl_label_1.nii.gz', 'gold_asl_label_1.nii.gz'))
        self.assertTrue(same_data('asl_label_2.nii.gz', 'gold_asl_label_2.nii.gz'))

    def tearDown(self):
        files = glob.glob('./test_data/asl*.nii.gz')
        [os.remove(f) for f in files]


class TestDiffusion(unittest.TestCase):

    def test_full_vol(self):
        run_pton('diffusion.PAR')
        self.assertTrue(same_data('diffusion.nii.gz', 'gold_diffusion.nii.gz'))

    def test_bvecs(self):
        run_pton('diffusion.PAR', '-d')
        self.assertTrue(same_data('diffusion_bval_1_bvec_7.nii.gz', 'gold_diffusion_bval_1_bvec_7.nii.gz'))
        self.assertTrue(same_data('diffusion_bval_2_bvec_1.nii.gz', 'gold_diffusion_bval_2_bvec_1.nii.gz'))
        self.assertTrue(same_data('diffusion_bval_2_bvec_4.nii.gz', 'gold_diffusion_bval_2_bvec_4.nii.gz'))
        self.assertTrue(same_data('diffusion_bval_2_bvec_7.nii.gz', 'gold_diffusion_bval_2_bvec_7.nii.gz'))

    def test_gtab(self):
        run_pton('diffusion.PAR', '-g')
        self.assertTrue(np.allclose(np.loadtxt('./test_data/diffusion.bval'),
                                    np.loadtxt('./test_data/gold_data/gold_diffusion.bval')))
        self.assertTrue(np.allclose(np.loadtxt('./test_data/diffusion.bvec'),
                                    np.loadtxt('./test_data/gold_data/gold_diffusion.bvec')))

    def tearDown(self):
        files = glob.glob('./test_data/diffusion*.nii.gz')
        [os.remove(f) for f in files]
        files = glob.glob('./test_data/diffusion*.bval')
        [os.remove(f) for f in files]
        files = glob.glob('./test_data/diffusion*.bvec')
        [os.remove(f) for f in files]


class TestDynamic(unittest.TestCase):

    def test_full_vol(self):
        run_pton('dynamic.PAR')
        self.assertTrue(same_data('dynamic.nii.gz', 'gold_dynamic.nii.gz'))

    def test_dynamic(self):
        run_pton('dynamic.PAR', '-s')
        self.assertTrue(same_data('dynamic_dynamic_1.nii.gz', 'gold_dynamic_dynamic_1.nii.gz'))
        self.assertTrue(same_data('dynamic_dynamic_5.nii.gz', 'gold_dynamic_dynamic_5.nii.gz'))
        self.assertTrue(same_data('dynamic_dynamic_10.nii.gz', 'gold_dynamic_dynamic_10.nii.gz'))

    def tearDown(self):
        files = glob.glob('./test_data/dynamic*.nii.gz')
        [os.remove(f) for f in files]


class TestEcho(unittest.TestCase):

    def test_full_vol(self):
        run_pton('multi_echo.PAR')
        self.assertTrue(same_data('multi_echo.nii.gz', 'gold_multi_echo.nii.gz'))

    def test_echo(self):
        run_pton('multi_echo.PAR', '-e')
        self.assertTrue(same_data('multi_echo_echo_1.nii.gz', 'gold_multi_echo_echo_1.nii.gz'))
        self.assertTrue(same_data('multi_echo_echo_6.nii.gz', 'gold_multi_echo_echo_6.nii.gz'))
        self.assertTrue(same_data('multi_echo_echo_12.nii.gz', 'gold_multi_echo_echo_12.nii.gz'))

    def test_type(self):
        run_pton('multi_echo.PAR', '-t')
        self.assertTrue(same_data('multi_echo_mag.nii.gz', 'gold_multi_echo_mag.nii.gz'))
        self.assertTrue(same_data('multi_echo_calculated.nii.gz', 'gold_multi_echo_calculated.nii.gz'))

    def tearDown(self):
        files = glob.glob('./test_data/multi_echo*.nii.gz')
        [os.remove(f) for f in files]


class TestScaling(unittest.TestCase):

    def test_fp(self):
        run_pton('image_type_mr.PAR')
        self.assertTrue(same_data('image_type_mr.nii.gz', 'gold_image_type_mr.nii.gz'))

    def test_ds(self):
        run_pton('image_type_mr.PAR', '-D')
        self.assertTrue(same_data('image_type_mr.nii.gz', 'gold_image_type_mr_display_scaling.nii.gz'))

    def test_ps(self):
        run_pton('image_type_mr.PAR', '-P')
        self.assertTrue(same_data('image_type_mr.nii.gz', 'gold_image_type_mr_no_scaling.nii.gz'))

    def tearDown(self):
        files = glob.glob('./test_data/image_type_mr*.nii.gz')
        [os.remove(f) for f in files]


class TestSimple(unittest.TestCase):

    def test_simple_3d(self):
        run_pton('simple_3D.PAR')
        self.assertTrue(same_data('simple_3D.nii.gz', 'gold_simple_3D.nii.gz'))

    def test_simple_2d(self):
        run_pton('simple_2D.PAR')
        self.assertTrue(same_data('simple_2D.nii.gz', 'gold_simple_2D.nii.gz'))

    def tearDown(self):
        files = glob.glob('./test_data/simple*.nii.gz')
        [os.remove(f) for f in files]


if __name__ == '__main__':
    unittest.main()
