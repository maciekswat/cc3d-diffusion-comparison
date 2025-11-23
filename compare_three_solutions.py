from pathlib import Path
import numpy as np
import csv

# ============================================
# INPUT DIRECTORIES
# ============================================

cc3d_folder = Path.home() / "solutions_CC3D"
manual_folder = Path.home() / "solutions_manual"
fipy_folder = Path.home() / "solutions_fipy"


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
    l1 = np.mean(np.abs(diff))
    l2 = np.sqrt(np.mean(diff**2))
    max_err = np.max(np.abs(diff))
    return l1, l2, max_err


# ============================================
# MAIN LOOP
# ============================================

def compare_all_steps():

    cc3d_files = sorted(cc3d_folder.glob("solution_*.csv"))
    manual_files = sorted(manual_folder.glob("solution_*.csv"))
    fipy_files = sorted(fipy_folder.glob("solution_*.csv"))

    steps = min(len(cc3d_files), len(manual_files), len(fipy_files))

    print(f"Comparing {steps} timesteps across 3 solvers\n")

    print("step | CC3D↔Manual L2 | CC3D↔FiPy L2 | Manual↔FiPy L2 | MaxErrorAny")
    print("-" * 90)

    stats = {
        "CC3D_MAN": [],
        "CC3D_FIPY": [],
        "MAN_FIPY": [],
    }

    for step in range(steps):

        A_cc3d = load_solution_csv(cc3d_files[step])
        A_manual = load_solution_csv(manual_files[step])
        A_fipy = load_solution_csv(fipy_files[step])

        l1_cm, l2_cm, max_cm = compute_metrics(A_cc3d, A_manual)
        l1_cf, l2_cf, max_cf = compute_metrics(A_cc3d, A_fipy)
        l1_mf, l2_mf, max_mf = compute_metrics(A_manual, A_fipy)

        stats["CC3D_MAN"].append(l2_cm)
        stats["CC3D_FIPY"].append(l2_cf)
        stats["MAN_FIPY"].append(l2_mf)

        global_max = max(max_cm, max_cf, max_mf)

        print(
            f"{step:04d} | "
            f"{l2_cm:14.6e} | "
            f"{l2_cf:14.6e} | "
            f"{l2_mf:14.6e} | "
            f"{global_max:12.6e}"
        )

    print("\n=== FINAL SUMMARY ===")
    print(f"Mean L2 CC3D ↔ Manual : {np.mean(stats['CC3D_MAN']):.6e}")
    print(f"Mean L2 CC3D ↔ FiPy   : {np.mean(stats['CC3D_FIPY']):.6e}")
    print(f"Mean L2 Manual ↔ FiPy : {np.mean(stats['MAN_FIPY']):.6e}")

    print("\nWorst disagreement observed:")
    print(f"Max CC3D ↔ Manual : {np.max(stats['CC3D_MAN']):.6e}")
    print(f"Max CC3D ↔ FiPy   : {np.max(stats['CC3D_FIPY']):.6e}")
    print(f"Max Manual ↔ FiPy : {np.max(stats['MAN_FIPY']):.6e}")


if __name__ == "__main__":
    compare_all_steps()
