import math

class Engine:
    BITS = [[0x01, 0x02, 0x04, 0x40], [0x08, 0x10, 0x20, 0x80]]

    @staticmethod
    def produit(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

    @staticmethod
    def compose(self, *matrices):  # compose(A, B, C) = A·B·C : C s'applique en premier
        R = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
        for matrix in matrices:
            R = self.produit(R, matrix)
        return R

    @staticmethod
    def rot_x(a):
        c, s = math.cos(a), math.sin(a)
        return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]

    @staticmethod
    def rot_y(a):
        c, s = math.cos(a), math.sin(a)
        return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]

    @staticmethod
    def translation(tx, ty, tz):
        return [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]]


    @staticmethod
    def applique(M, p):
        v = (p[0], p[1], p[2], 1.0)
        return tuple(sum(M[i][k] * v[k] for k in range(4)) for i in range(3))

    @staticmethod
    def projette(p):
        x, y, z = p
        return x / -z, y / -z

    def point(self, x, y, scene):
        x, y = round(x), round(y)
        if 0 <= x < scene.cols * 2 and 0 <= y < scene.rows * 4:
            scene.cases[y // 4][x // 2] |= self.BITS[x % 2][y % 4]

    def line(self, a, b, scene):  # algorithme de Bresenham
        x0, y0, x1, y1 = round(a[0]), round(a[1]), round(b[0]), round(b[1])
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.point(x0, y0, scene)
            if (x0, y0) == (x1, y1):
                break
            e2 = 2 * err
            if e2 >= dy: err += dy; x0 += sx
            if e2 <= dx: err += dx; y0 += sy

    def simple_line(self, a, b, scene):
        x0, y0, x1, y1 = round(a[0]), round(a[1]), round(b[0]), round(b[1])
        n = max(abs(x1 - x0), abs(y1 - y0), 1)  # nombre de pas
        for i in range(n + 1):
            t = i / n
            self.point(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, scene)

    def render(self, t, scene, simple_line=False):
        scene.initCases()
        for mesh in scene.meshes:
            matrix = self.compose(self, self.translation(0, 0, -4.5), self.rot_y(t), self.rot_x(0.6 * t + 0.4))
            pts = []
            for s in mesh.VERTICES:
                x, y = self.projette(self.applique(matrix, s))
                pts.append((scene.cols + scene.echelle * x, scene.rows * 2 - scene.echelle * y))  # centre de la toile, y vers le bas
            for i, j in mesh.ARETES:
                if simple_line:
                    self.simple_line(pts[i], pts[j], scene)
                else:
                    self.line(pts[i], pts[j], scene)
        return str(scene)