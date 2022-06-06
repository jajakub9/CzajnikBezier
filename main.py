import math
import os

POINTS_FILENAME = os.path.dirname(os.path.abspath(__file__)) + "\\" + "points.txt"
OUT_POINTS_FILENAME = os.path.dirname(os.path.abspath(__file__)) + "\\" + "out_points.txt"
MATRIX_R = MATRIX_C = 4


def binomial_coefficient(n, k):
    if k == 1: return n

    n_factorial = 1
    for x in range(1, n):
        n_factorial += n_factorial * x

    k_factorial = 1
    for x in range(1, k):
        k_factorial += k_factorial * x

    nk_factorial = 1
    for x in range(1, n - k):
        nk_factorial += nk_factorial * x

    return n_factorial / (k_factorial * nk_factorial)


def bernstein(n, i, t):
    return binomial_coefficient(n, i) * math.pow(t, i) * math.pow(1 - t, n - i)


def bezier_surface(points, steps):
    n = len(points) - 1
    result = []

    def point(u, v, near_points):
        x = 0
        y = 0
        z = 0
        for i in range(MATRIX_R):
            bi = bernstein(MATRIX_R - 1, i, v)
            for j in range(MATRIX_C):
                bj = bernstein(MATRIX_C - 1, j, u)
                if len(near_points[i][j]) != 0:
                    x += float(near_points[i][j][0]) * bi * bj
                    y += float(near_points[i][j][1]) * bi * bj
                    z += float(near_points[i][j][2]) * bi * bj

        return [round(x, 5), round(y, 5), round(z, 5)]

    z = 0
    for i in range(0, int((n + 1) / (MATRIX_C * MATRIX_R))):

        # construct matrix for this chunk
        matrix = [[[] for i in range(MATRIX_C)] for i in range(MATRIX_R)]
        for x in range(0, MATRIX_R):
            for y in range(0, MATRIX_C):
                if z <= n + 1:
                    matrix[x][y] = points[z]
                    z += 1

        fact = (1.0 / steps)
        for u in range(0, steps + 1):
            u_ = u * fact
            for v in range(0, steps + 1):
                v_ = v * fact
                result.append(point(u_, v_, matrix))

    return result


# return (x, y, z)
def read_points(filename):
    file = open(filename, "r")
    points = []
    for line in file.readlines():
        points.append(line.split())
    return points


def convert_points(points):
    out = ""
    for point in points:
        for point_pos in point:
            out += str(point_pos) + " "
        out += "\n"
    return out


def write_to_file(points, filename):
    file = open(filename, "w")
    file.write(points)


points = bezier_surface(read_points(POINTS_FILENAME), 60)
write_to_file(convert_points(points), OUT_POINTS_FILENAME)