import sys, time

from Cube import Cube
from Engine import Engine
from Scene import Scene

engine = Engine()
scene = Scene(40, 20, 36) # 60 x 40 points
# scene = Scene(80, 40, 72) # 120 x 80 points
scene.addMesh(Cube(2))

t = 0.0
print("\033[?25l", end="", flush=True)  # masquer le curseur
while True:
    sys.stdout.write(
        "\033[H\033[2J\033[3J" +
        engine.render(t, scene) +
        "\n" +
        engine.render(t, scene, True) +
        "\n"
    )
    sys.stdout.flush()
    t += 0.005
    time.sleep(0.03)
