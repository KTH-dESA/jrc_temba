# JRC TEMBA Analysis

To reproduce the results, run `bash run_analysis.sh`

This repository contains all the scripts and data necessary to reproduce the
work for JRC TEMBA project.

## Setup and Installation

To run this analysis you need to install GLPK and one of CBC or CPLEX

You should also have Python 3 environment setup with the following dependencies:

- `xlrd`

## Folder structure

- Input data is stored in the `input_data` folder
- The OSeMOSYS model file is stored in `model` folder
- Temporary output data is stored in the `output_data` folder
- Final results are stored in `results`
- All the scripts for intermediate processing are stored in the `scripts` folder
