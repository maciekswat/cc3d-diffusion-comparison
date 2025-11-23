from cc3d.core.PySteppables import *
import os
from pathlib import Path


class diffusion_2D_scaleSteppable(SteppableBasePy):

    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        # results are written to solutions_CC3D  inside your  home folder
        self.output_folder = Path.home().joinpath( "solutions_CC3D")
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def start(self):
        # create output folder once
        os.makedirs(self.output_folder, exist_ok=True)

    def write_solution_to_file(self, field, step):
        filename = f"solution_{step:03d}.csv"
        filepath = self.output_folder.joinpath(filename)

        with open(filepath, "w") as f:
            f.write("x,y,z,value\n")

            # Assuming 2D field, z is always 0
            for x in range(self.dim.x):
                for y in range(self.dim.y):
                    f.write(f"{x},{y},0,{field[x, y, 0]}\n")

        print(f"CC3D wrote: {filepath}")

    def step(self, mcs):

        fgf = self.field.FGF

        # Off-by-one correction to match your Python solver
        step_index = mcs - 1

        if step_index < 0:
            return

        print(
            f"mcs={mcs} step={step_index} center={fgf[50,50,0]} "
            f"probe={fgf[20,45,0]}"
        )

        #  Write one solution per diffusion step
        self.write_solution_to_file(fgf, step_index)

    def finish(self):
        pass
