# PAR to nii
[![Build Status](https://travis-ci.com/alexdaniel654/PAR_to_nii.svg?branch=master)](https://travis-ci.com/alexdaniel654/PAR_to_nii)

pton (p-to-n or par-to-nifti) is a command line utility that converts Philips PAR/REC format data into compressed nifti data. This tool is designed as an alternative to the popular ptoa.exe which outputs the now outdated analyze format.

## Features
This software, at it's most basic, takes a PAR/REC file and converts the whole volume into a compressed nifti file. One of the major motivations for writing this software is that, unlike ptoa, it keeps the affine information from the PAR/REC making working between multiple geometries far easier.

### Saving volumes in different files
It can often be useful to have different files for each volume type, be that saving the magnitude and phase separately or saving each label from ASL data in a different file. For a full explanation of the volume separations available look in the usage section below.

### Changing data scaling
By default, pton saves the nifti files as floating point scaling which is the most useful for scientific purposes (for a start phase goes between -pi and pi). It is possible to save the nifti as either the values from the REC file i.e. no scaling or with display value scaling.

### Extracting gradient information
The gradient information from a DWI/DTI scan is saved in the PAR file. pton can extract this info and save it as a text file which is a. human readable and b. readable by FSL.

## Usage

To use pton open command prompt and use the syntax below. Any number of volume separation flags can be used to subdivide the file as much as you want i.e. for the example below the magnitude and phase of each echo time are saved in a different nifti file.

``.\pton.exe data.PAR -etv``

### Full list of flags available

| Short Flag | Long Flag       | Usage                                                                       |
|------------|-----------------|-----------------------------------------------------------------------------|
| -h         | --help          | Shows the available flags                                                   |
| -e         | --echo          | Saves each echo as a different file                                         |
| -p         | --phase         | Save each cardiac phase as a different file                                 |
| -d         | --diffusion     | Save each gradient direction as a different file                            |
| -l         | --label         | Save each label as a different file                                         |
| -t         | --type_mr       | Save each image type (mag, phase, re, im or calculated) as a different file |
| -s         | --dynamic_scan  | Save dynamic as a different file                                            |
| -g         | --gtab          | Save the gradient directions and b values to text documents                 |
| -P         | --pixel_value   | Data scaling as per the REC file                                            |
| -D         | --display_value | Data scaling as displayed on console                                        |
| -v         | --verbose       | Display additional information to command-line                              |
