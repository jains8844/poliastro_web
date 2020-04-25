from poliastro.plotting import OrbitPlotter3D
from poliastro.bodies import Earth
from poliastro.examples import iss
plot = OrbitPlotter3D()
plot._attractor = Earth
r=iss.r
figure1 = plot._plot_position(r, "HEY", ["rgb(31, 119, 180)"])
