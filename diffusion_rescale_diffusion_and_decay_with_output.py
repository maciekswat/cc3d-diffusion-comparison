import numpy as np
import plotly.graph_objects as go
import math
from pathlib import Path

Nx, Ny = 100, 100
dx = dy = 1.0

D = 1.0
k = 0.001
dt = 1.0
steps = 100

D_base = 0.2

substeps = max(1, math.ceil(D / D_base))
D_sub = D / substeps
k_sub = k / substeps

print(f"Target D={D}, k={k}")
print(f"Substeps = {substeps}")
print(f"Per-substep D = {D_sub}, k = {k_sub}")

C = np.zeros((Nx, Ny))
C[Nx//2, Ny//2] = 2000.0

def apply_no_flux_boundary(C):
    C[0, :] = C[1, :]
    C[-1, :] = C[-2, :]
    C[:, 0] = C[:, 1]
    C[:, -1] = C[:, -2]
    return C

folder_name = Path.home().joinpath(f"solutions_manual")
folder_name.mkdir(parents=True, exist_ok=True)

def write_solution_to_file(C, step):
    filename = f"solution_{step:03d}.csv"
    filepath = folder_name.joinpath(filename)
    with open(filepath, "w") as f:
        f.write("x,y,z,value\n")
        for y in range(Ny):
            for x in range(Nx):
                f.write(f"{x},{y},0,{C[x,y]}\n")
    print(f"Wrote {filepath}")

for t in range(steps):
    for s in range(substeps):
        C_new = C.copy()
        laplacian = (
            C[2:, 1:-1] + C[:-2, 1:-1] +
            C[1:-1, 2:] + C[1:-1, :-2] -
            4 * C[1:-1, 1:-1]
        )
        C_new[1:-1, 1:-1] += dt * (
            D_sub * laplacian - k_sub * C[1:-1, 1:-1]
        )
        C = apply_no_flux_boundary(C_new)
    print(f"step={t} center={C[Nx//2, Ny//2]:.6f} probe={C[20,45]:.6f}")
    write_solution_to_file(C, t)

# fig = go.Figure(data=go.Heatmap(z=C, colorbar=dict(title="Concentration")))
# fig.update_layout(title=f"2D Diffusion (D={D}, k={k}, substeps={substeps})",
#                   xaxis_title="X", yaxis_title="Y", width=400, height=400)
# fig.show()
