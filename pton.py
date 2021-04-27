# -*- coding: utf-8 -*-
"""
Created: 08/11/2018
Last update: 12/11/2018
Alex Daniel, Sir Peter Mansfield Imaging Centre, The University of Nottingham, 2018.

pton (p-to-n or par-to-nifti) converts Philips PAR/REC format data into compressed nifti data. This tool is designed as
an alternative to the popular ptoa.exe which outputs the now outdated analyze format.

Example: python pton.py /path/to/diffusion_data.PAR -dgv
The above command will convert the data diffusion_data.PAR to multiple compressed nifti files, one for each gradient
direction/b-value. It will also save the gradient directions and b-values into text files called diffusion_data.bvec and
diffusion_data.bval and print lost of information into the terminal while it does it.

For a more comprehensive list of features/options run python pton.py -h
"""

from __future__ import print_function
from optparse import OptionParser

# Pars options
parser = OptionParser()
parser.add_option('-e', '--echo', action='store_true', default=False, dest='multi_echo',
                  help='Save each echo as a different file')
parser.add_option('-p', '--phase', action='store_true', default=False, dest='multi_phase',
                  help='Save each cardiac phase as a different file')
parser.add_option('-d', '--diffusion', action='store_true', default=False, dest='diffusion',
                  help='Save each gradient direction as a different file')
parser.add_option('-l', '--label', action='store_true', default=False, dest='label',
                  help='Save each label as a different file')
parser.add_option('-t', '--type_mr', action='store_true', default=False, dest='multi_type',
                  help='Save each image type (mag, phase, re, im or calculated) as a different file')
parser.add_option('-s', '--dynamic_scan', action='store_true', default=False, dest='dynamic',
                  help='Save dynamic as a different file')
parser.add_option('-g', '--gtab', action='store_true', default=False, dest='gradient',
                  help='Save the gradient directions and b values to text documents')
parser.add_option('-P', '--pixel_value', action='store_true', default=False, dest='pixel_value',
                  help='Data scaling as per the REC file')
parser.add_option('-D', '--display_value', action='store_true', default=False, dest='display_value',
                  help='Data scaling as displayed on console')
parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose',
                  help='Display additional information to command-line')
(options, args) = parser.parse_args()

import nibabel as nib
import numpy as np
import sys

verboseprint = print if options.verbose else lambda *a, **k: None

in_name = sys.argv[1]

# Load the image (with appropriate scaling)
if options.pixel_value:
    img = nib.load(in_name, strict_sort=True, permit_truncated=True)
    verboseprint('Importing with no data scaling')
elif options.display_value:
    img = nib.load(in_name, strict_sort=True, scaling='dv', permit_truncated=True)
    verboseprint('Importing with display value scaling')
else:
    img = nib.load(in_name, strict_sort=True, scaling='fp', permit_truncated=True)
    verboseprint('Importing with floating point scaling')

hdr = img.header
try:
    vols = img.shape[3]
except IndexError:
    vols = 1
sort = hdr.get_volume_labels()

scan_type = {}

# Establish how many output files there are going to end up being
if 'echo number' in sort:
    if options.multi_echo:
        scan_type['echos'] = np.unique(sort['echo number'])
    else:
        scan_type['echos'] = 0
        sort['echo number'] = np.zeros(vols)
else:
    scan_type['echos'] = 0
    sort['echo number'] = np.zeros(vols)

if 'cardiac phase number' in sort:
    if options.multi_phase:
        scan_type['phases'] = np.unique(sort['cardiac phase number'])
    else:
        scan_type['phases'] = 0
        sort['cardiac phase number'] = np.zeros(vols)
else:
    scan_type['phases'] = 0
    sort['cardiac phase number'] = np.zeros(vols)

if 'gradient orientation number' in sort:
    if options.diffusion:
        scan_type['bvecs'] = np.unique(sort['gradient orientation number'])
        scan_type['bvals'] = np.unique(sort['diffusion b value number'])
    else:
        scan_type['bvecs'] = 0
        scan_type['bvals'] = 0
        sort['gradient orientation number'] = np.zeros(vols)
        sort['diffusion b value number'] = np.zeros(vols)
else:
    scan_type['bvecs'] = 0
    scan_type['bvals'] = 0
    sort['gradient orientation number'] = np.zeros(vols)
    sort['diffusion b value number'] = np.zeros(vols)

if 'label type' in sort:
    if options.label:
        scan_type['labels'] = np.unique(sort['label type'])
    else:
        scan_type['labels'] = 0
        sort['label type'] = np.zeros(vols)
else:
    scan_type['labels'] = 0
    sort['label type'] = np.zeros(vols)

if 'image_type_mr' in sort:
    if options.multi_type:
        scan_type['types'] = np.unique(sort['image_type_mr'])
    else:
        scan_type['types'] = 0
        sort['image_type_mr'] = np.zeros(vols)
else:
    scan_type['types'] = 0
    sort['image_type_mr'] = np.zeros(vols)

if 'dynamic scan number' in sort:
    if options.dynamic:
        scan_type['dynamic'] = np.unique(sort['dynamic scan number'])
    else:
        scan_type['dynamic'] = 0
        sort['dynamic scan number'] = np.zeros(vols)
else:
    scan_type['dynamic'] = 0
    sort['dynamic scan number'] = np.zeros(vols)
    
# Load the image data
data = img.get_fdata()

if len(data.shape) == 3:
    data = np.expand_dims(data, 3)

for echo in np.nditer(scan_type['echos']):
    for phase in np.nditer(scan_type['phases']):
        for bval in np.nditer(scan_type['bvals']):
            for bvec in np.nditer(scan_type['bvecs']):
                for label in np.nditer(scan_type['labels']):
                    for type_mr in np.nditer(scan_type['types']):
                        for dynamic in np.nditer(scan_type['dynamic']):
                            # Filter the data to only be there specific volume(s) we want to save
                            sub_data = data[:, :, :, np.logical_and.reduce((sort['echo number'] == echo,
                                                                            sort['cardiac phase number'] == phase,
                                                                            sort['diffusion b value number'] == bval,
                                                                            sort['gradient orientation number'] == bvec,
                                                                            sort['label type'] == label,
                                                                            sort['image_type_mr'] == type_mr,
                                                                            sort['dynamic scan number'] == dynamic))]

                            if sub_data.shape[3] != 0:
                                # Make an output file name
                                out_name = in_name[:-4]
                                if options.multi_echo:
                                    out_name += '_echo_' + str(echo)
                                if options.multi_phase:
                                    out_name += '_phase_' + str(phase)
                                if options.diffusion:
                                    out_name += '_bval_' + str(bval) + '_bvec_' + str(bvec)
                                if options.label:
                                    out_name += '_label_' + str(label)
                                if options.dynamic:
                                    out_name += '_dynamic_' + str(dynamic)
                                if options.multi_type:
                                    if type_mr == -1:
                                        out_name += '_calculated'
                                    elif type_mr == 0:
                                        out_name += '_mag'
                                    elif type_mr == 1:
                                        out_name += '_real'
                                    elif type_mr == 2:
                                        out_name += '_imag'
                                    elif type_mr == 3:
                                        out_name += '_phase'
                                out_name += '.nii.gz'
                                print(out_name)

                                # Print other useful information if verbose mode is on
                                verboseprint('Volume shape = ' + str(sub_data.shape[0])
                                             + 'x' + str(sub_data.shape[1])
                                             + 'x' + str(sub_data.shape[2])
                                             + 'x' + str(sub_data.shape[3]))
                                verboseprint('echo = ' + str(echo))
                                verboseprint('phase = ' + str(phase))
                                verboseprint('bval = ' + str(bval))
                                verboseprint('bvec = ' + str(bvec))
                                verboseprint('label = ' + str(label))
                                verboseprint('dynamic = ' + str(dynamic))
                                verboseprint('type = ' + str(type_mr) + '\n')

                                # Make the nifti image object and save it
                                img_out = nib.Nifti1Image(sub_data, img.affine)
                                nib.save(img_out, out_name)

# Save the gradient and b-value information as text files
if options.gradient:
    # TODO add error if no bvals/bvecs present
    bvals, bvecs = hdr.get_bvals_bvecs()
    np.savetxt(in_name[:-3] + 'bvec', bvecs.T, fmt='%.3f')
    np.savetxt(in_name[:-3] + 'bval', np.expand_dims(bvals, 1).T, fmt='%.0f')
