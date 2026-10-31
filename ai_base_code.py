"""Cube filaire 3D qui tourne dans le terminal.
Matrices 4x4 homogènes écrites à la main + perspective + tracé Braille (Bresenham).
Usage :  python3 cube3d.py          (animation, Ctrl+C pour quitter)
         python3 cube3d.py demo     (affiche quelques images fixes)
"""
import math, sys, time


# ---------- algèbre linéaire (matrices 4x4 en listes de listes) ----------
def produit(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def compose(*Ms):  # compose(A, B, C) = A·B·C : C s'applique en premier
    R = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    for M in Ms:
        R = produit(R, M)
    return R


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]


def translation(tx, ty, tz):
    return [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]]


def applique(M, p):
    v = (p[0], p[1], p[2], 1.0)
    return tuple(sum(M[i][k] * v[k] for k in range(4)) for i in range(3))


def projette(p, f=2.5):
    """Perspective : la caméra est à l'origine et regarde vers -z. On divise par la profondeur."""
    x, y, z = p
    return f * x / -z, f * y / -z


# ---------- toile Braille (2x4 points par case) ----------
BITS = [[0x01, 0x02, 0x04, 0x40], [0x08, 0x10, 0x20, 0x80]]


class Toile:
    def __init__(self, cols, rows):
        self.c, self.r = cols, rows
        self.cases = [[0] * cols for _ in range(rows)]

    def point(self, x, y):
        x, y = round(x), round(y)
        if 0 <= x < self.c * 2 and 0 <= y < self.r * 4:
            self.cases[y // 4][x // 2] |= BITS[x % 2][y % 4]

    def ligne(self, a, b):  # algorithme de Bresenham
        x0, y0, x1, y1 = round(a[0]), round(a[1]), round(b[0]), round(b[1])
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.point(x0, y0)
            if (x0, y0) == (x1, y1):
                break
            e2 = 2 * err
            if e2 >= dy: err += dy; x0 += sx
            if e2 <= dx: err += dx; y0 += sy

    def __str__(self):
        return "\n".join("".join(chr(0x2800 + v) for v in l) for l in self.cases)


# ---------- le cube ----------
SOMMETS = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
ARETES = [(i, j) for i in range(8) for j in range(i + 1, 8) if bin(i ^ j).count("1") == 1]  # 12 arêtes


def image(t, cols=40, rows=20, echelle=36):
    M = compose(translation(0, 0, -4.5), rot_y(t), rot_x(0.6 * t + 0.4))
    pts = []
    for s in SOMMETS:
        x, y = projette(applique(M, s))
        pts.append((cols + echelle * x, rows * 2 - echelle * y))  # centre de la toile, y vers le bas
    toile = Toile(cols, rows)
    for i, j in ARETES:
        toile.ligne(pts[i], pts[j])
    return str(toile)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        for t in (0.0, 0.5, 1.0):
            print("t = %.1f" % t);
            print(image(t));
            print()
    else:
        try:
            t = 0.0
            while True:
                sys.stdout.write("\033[H\033[J" + image(t) + "\n");
                sys.stdout.flush()
                t += 0.04;
                time.sleep(0.03)
        except KeyboardInterrupt:
            pass
