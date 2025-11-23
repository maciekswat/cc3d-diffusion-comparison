# Diffusion Solver Comparison

This project provides **three independent diffusion solvers** and a validation pipeline:

1. **Manual finite difference solver** (explicit, substepped, CSV output)  
2. **FiPy-based solver** (implicit reference implementation)  
3. **CompuCell3D (CC3D) simulation** (production-grade PDE solver)

You can compare all three using the included 3-way comparison script.

---

## Setup

### 1. Install Conda

You only need **one** Conda distribution:

- If you already have **Anaconda** or **Miniconda** → you can use it directly  
- If you do NOT have Conda → install **Miniforge** (recommended)

Miniforge download:  
https://github.com/conda-forge/miniforge

---

### 2. Create and activate environment

From the project root:

```bash
conda env create -f environment.yml
conda activate diffusion-env
```

---

## Simulation Workflow (Required Order)

### Step 1 — Run CC3D simulation

Open the included CC3D simulation in **CompuCell3D Player** and run it.

The CC3D steppable will automatically write results to:

```
~/solutions_CC3D/
└── solution_000.csv
└── solution_001.csv
└── ...
```

---

### Step 2 — Run manual solver

```bash
python diffusion_rescale_diffusion_and_decay_with_output.py
```

This generates:

```
~/solutions_manual/
└── solution_000.csv
└── solution_001.csv
└── ...
```

---

### Step 3 — Run FiPy solver

```bash
python fipy_solver_demo.py
```

This generates:

```
~/solutions_fipy/
└── solution_000.csv
└── solution_001.csv
└── ...
```

---

### Step 4 — Run 3-way comparison

```bash
python compare_three_solvers.py
```

This will compute per-timestep error metrics between:

- CC3D ↔ Manual  
- CC3D ↔ FiPy  
- Manual ↔ FiPy  

and print:
- L2 error per timestep  
- Mean total error  
- Worst disagreement observed

---

## Expected Output Summary

```
Comparing 100 timesteps across 3 solvers

step | CC3D↔Manual L2 | CC3D↔FiPy L2 | Manual↔FiPy L2
------------------------------------------------------
0000 | 2.112e-02 | 4.998e-02 | 3.884e-02
0001 | 1.842e-02 | 4.233e-02 | 3.112e-02
...

=== FINAL SUMMARY ===
Mean L2 CC3D ↔ Manual : 1.22e-03
Mean L2 CC3D ↔ FiPy   : 2.99e-03
Mean L2 Manual ↔ FiPy : 2.10e-03
```

---

## Notes

- CC3D does not run diffusion at MCS=0 — outputs start at MCS=1  
- Output filenames are aligned so timestep 9 = MCS 10  
- All solvers assume no-flux boundary conditions  
- Manual solver uses diffusion and decay rescaling for stability  

---

## Purpose

This project validates:

- Numerical correctness of the explicit solver  
- Stability and accuracy of CC3D PDE solver  
- Agreement against FiPy reference implementation  

This comparison framework is suitable for:

- Solver benchmarking  
- Reproducible scientific validation  
- Methodology documentation  
- Publications and technical reports  




