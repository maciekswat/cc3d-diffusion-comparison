# Diffusion Solver Comparison

This project provides two diffusion solvers:
1. Manual finite difference solver with substepping.
2. FiPy-based solver for validation.

## Setup

### Install Miniforge
Download from:
https://github.com/conda-forge/miniforge

### Create environment
conda env create -f environment.yml
conda activate diffusion-env

### Run solvers
python diffusion_rescale_diffusion_and_decay_with_output.py
python fipy_solver_demo.py
