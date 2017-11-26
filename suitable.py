from algorithms import *
from high_potential_area import *
from maps import Map


class Suitable:
    def __init__(self, list_algorithms=[]):
        self.list_algorithms = list_algorithms

    def attach_maps(self):
        algs = self.list_algorithms

        res = Map()

        # ---- make empty 2D res ----
        for i in range(algs[0]):
            res.matrix.append([])
            for j in range(algs[0][i]):
                res.append(res.matrix[i].append(res.no_data_value))

        # ----
        for alg in algs:
            for i in range(len(alg)):
                for j in range(len(alg[i])):
                    if alg[i][j] == 1:
                        res.matrix[i][j] += alg.tag





