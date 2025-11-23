from pathlib import Path
import numpy as np
import csv

# ============================================
# USER INPUT DIRECTORIES
# ============================================

cc3d_folder = Path.home() / "solutions_CC3D"
manual_folder = Path.home() / "solutions_manual"
# fipy_folder = Path.home() / "solutions_fipy"

# ============================================
# CSV READER
# ============================================

def load_solution_csv(path: Path, Nx=100, Ny=100):
    field = np.zeros((Nx, Ny))

    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header

        for row in reader:
            x, y, z, value = row
            field[int(x), int(y)] = float(value)

    return field


# ============================================
# METRICS
# ============================================

def compute_metrics(A, B):
    diff = A - B

    l2 = np.sqrt(np.mean(diff**2))
    l1 = np.mean(np.abs(diff))
    max_err = np.max(np.abs(diff))

    return l1, l2, max_err


# ============================================
# MAIN COMPARISON LOOP
# ============================================

def compare_all_steps():
    cc3d_files = sorted(cc3d_folder.glob("solution_*.csv"))
    manual_files = sorted(manual_folder.glob("solution_*.csv"))

    steps = min(len(cc3d_files), len(manual_files))

    print(f"Comparing {steps} timesteps")
    print("step |   L1 error   |   L2 error   |   Max error")
    print("-" * 55)

    total_l1 = []
    total_l2 = []
    total_max = []

    for step in range(steps):
        file_cc3d = cc3d_files[step]
        file_manual = manual_files[step]

        A = load_solution_csv(file_cc3d)
        B = load_solution_csv(file_manual)

        l1, l2, max_err = compute_metrics(A, B)

        total_l1.append(l1)
        total_l2.append(l2)
        total_max.append(max_err)

        print(f"{step:04d} | {l1:12.6e} | {l2:12.6e} | {max_err:12.6e}")

    print("\n=== FINAL SUMMARY ===")
    print(f"Mean L1 Error:  {np.mean(total_l1):.6e}")
    print(f"Mean L2 Error:  {np.mean(total_l2):.6e}")
    print(f"Max Error Ever: {np.max(total_max):.6e}")


if __name__ == "__main__":
    compare_all_steps()
