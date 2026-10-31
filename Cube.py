from Scene import Scene
class Cube:
    def __init__(self, size=1):
        self.VERTICES = [(x*size, y*size, z*size) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
        self.ARETES = [(i, j) for i in range(8) for j in range(i + 1, 8) if bin(i ^ j).count("1") == 1]