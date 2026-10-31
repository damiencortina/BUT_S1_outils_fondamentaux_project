class Scene:
    def __init__(self, cols, rows, echelle):
        self.cols = cols
        self.rows = rows
        self.echelle = echelle
        self.meshes = []
        self.initCases()

    def initCases(self):
        self.cases = [[0] * self.cols for _ in range(self.rows)]

    def addMesh(self, mesh):
        self.meshes.append(mesh)

    def render(self):
        for mesh in self.meshes:
            mesh.render(self)

    def __str__(self):
        return "\n".join("".join(chr(0x2800 + v) for v in l) for l in self.cases)