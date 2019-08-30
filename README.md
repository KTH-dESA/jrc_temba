# JRC TEMBA Analysis

You can view the source code for this workflow in the [repository](https://github.com/KTH-dESA/jrc_temba)

This repository contains all the scripts and data necessary to reproduce the
work for JRC TEMBA project.

## Setup and Installation

To run this analysis you need to install GLPK and a solver such as CBC, CPLEX or Gurobi

You should also have Python >=3.6 environment setup with the following dependencies ideally
using miniconda so that snakemake can manage custom environments for each of the workflow tasks:

- `pandas`
- `xlrd`
- [`snakemake`](https://snakemake.readthedocs.io/en/stable/index.html)

## Running the TEMBA workflow

To run the workflow with snakemake, type the command `snakemake`.

To perform a dry run, use the flag `-n` and to run the workflow in parallel, use the flag `-j` and pass the (optional)
number of threads to use e.g. `snakemake -j 8`.

## Folder structure

- Input data are stored in `.xlsx` Excel files in the `input_data` folder
- A modified OSeMOSYS model file is stored in `model` folder
- Temporary output data is stored in the `output_data` folder
- Final results are stored in `results`
- All the scripts for intermediate processing are stored in the `scripts` folder

## Licensing

- Data is released under the terms of a CC-BY 4.0 License Agreement.
- A modified copy of OSeMOSYS is redistribruted in this repository under Apache 2.0 license agreement, 
  a copy of which can be found in the `model` folder

## Citation

If you wish to use, extend or otherwise build upon the work contained within this repository, you are
welcome to do so, provided you abide by the terms of the licenses detailed above.

Please cite this work in the following manner:

    Pappis, I., Howells, M., Sridharan, V., Usher, W., Shivakumar, A., Gardumi, F., Ramos, E., 2019,
    Energy demand projections for African countries: The Energy Model Base for Africa (TEMBA)
