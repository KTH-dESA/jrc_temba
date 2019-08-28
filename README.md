# JRC TEMBA Analysis

To reproduce the results, run `bash run_analysis.sh`

This repository contains all the scripts and data necessary to reproduce the
work for JRC TEMBA project.

## Setup and Installation

To run this analysis you need to install GLPK and one of CBC or CPLEX

You should also have Python >=3.6 environment setup with the following dependencies:

- `pandas`
- `xlrd`
- [`snakemake`](https://snakemake.readthedocs.io/en/stable/index.html)

## Running the TEMBA workflow

To run the workflow with snakemake, type the command `snakemake`.

To perform a dry run, use the flag `-n` and to run the workflow in parallel, use the flag `-j` and pass the (optional)
number of threads to use e.g. `snakemake -j 8`.

## Folder structure

- Input data are stored in `.xlsx` Excel files in the `input_data` folder
- The OSeMOSYS model file is stored in `model` folder
- Temporary output data is stored in the `output_data` folder
- Final results are stored in `results`
- All the scripts for intermediate processing are stored in the `scripts` folder
