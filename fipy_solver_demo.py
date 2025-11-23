import numpy as np
from fipy import CellVariable, Grid2D, DiffusionTerm, ImplicitSourceTerm, TransientTerm
from pathlib import Path

Nx = Ny = 100
D = 1.0
k = 0.001
steps = 200
dt = 1.0

# ===============================
# SETUP OUTPUT FOLDER
# ===============================

output_folder = Path.home() / "solutions_fipy"
output_folder.mkdir(parents=True, exist_ok=True)


def write_solution_to_file(field_2d: np.ndarray, step: int):
    filename = f"solution_{step:03d}.csv"
    filepath = output_folder / filename

    with open(filepath, "w") as f:
        f.write("x,y,z,value\n")
        for y in range(Ny):
            for x in range(Nx):
                f.write(f"{x},{y},0,{field_2d[x, y]}\n")

    print(f"FiPy wrote {filepath}")


# ===============================
# FIPY SETUP
# ===============================

mesh = Grid2D(dx=1.0, dy=1.0, nx=Nx, ny=Ny)
C = CellVariable(mesh=mesh, value=0.0)

center_index = (Nx//2) + (Ny//2) * Nx
probe_index = 20 + 45 * Nx

C.value[center_index] = 2000.0

eq = TransientTerm() == DiffusionTerm(coeff=D) - ImplicitSourceTerm(coeff=k)

# ===============================
# SOLVER LOOP
# ===============================

for t in range(steps):
    eq.solve(var=C, dt=dt)

    # reshape FiPy internal 1D array to 2D field
    C_fipy = np.array(C.value).reshape((Nx, Ny))

    print(
        f"step={t} center={C_fipy[Nx//2, Ny//2]:.3f} "
        f"probe={C_fipy[20,45]:.3f}"
    )

    #  write per-step solution
    write_solution_to_file(C_fipy, t)

# import numpy as np
# from fipy import CellVariable, Grid2D, DiffusionTerm, ImplicitSourceTerm, TransientTerm
#
# Nx = Ny = 100
# D = 1.0
# k = 0.001
# steps = 200
# dt = 1.0
#
# mesh = Grid2D(dx=1.0, dy=1.0, nx=Nx, ny=Ny)
# C = CellVariable(mesh=mesh, value=0.0)
#
# center_index = (Nx//2) + (Ny//2) * Nx
# probe_index = 20 + 45 * Nx
#
# C.value[center_index] = 2000.0
#
# eq = TransientTerm() == DiffusionTerm(coeff=D) - ImplicitSourceTerm(coeff=k)
#
# for t in range(steps):
#     eq.solve(var=C, dt=dt)
#     print(f"step={t} center={C.value[center_index]:.3f} probe={C.value[probe_index]:.3f}")
#
# C_fipy = np.array(C.value).reshape((Ny, Nx))
