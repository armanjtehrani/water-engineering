class Map:
    def __init__(self):
        self.n_cols = 0
        self.n_rows = 0
        self.xll_corner = 0
        self.yll_corner = 0
        self.cell_size = 0
        self.no_data_value = -9999
        self.matrix = [[]]

    def __str__(self):
        str_data = ""
        str_data += "row nums:" + str(self.n_rows) + '\n'
        str_data += "col nums:" + str(self.n_cols) + '\n'
        str_data += "xll_corner:" + str(self.xll_corner) + '\n'
        str_data += "yll_corner:" + str(self.yll_corner) + '\n'
        str_data += "cell_size:" + str(self.cell_size) + '\n'
        str_data += "no_data_value:" + str(self.no_data_value) + '\n'
        str_data += '\n\nmap:\n'
        for i in range(len(self.matrix)):
            str_data += str(self.matrix[i])
        return str_data


class SoilMap:
    class VALUES:
        SAND = 1
        LOAMY_SAND = 2
        SANDY_LOAM = 3
        SILT_LOAM = 4
        SILT = 5
        LOAM = 6
        SANDY_CLAY_LOAM = 7
        SILT_CLAY_LOAM = 8
        CLAY_LOAM = 9
        SANDY_CLAY = 10
        SILT_CLAY = 11
        CLAY = 12

    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('soil map:\n' + str(self.map))


class LandUseMap:
    class VALUES:
        EVERGREEN_NEEDLE_LEAF_FOREST = 1
        EVERGREEN_BROAD_LEAF_FOREST = 2
        DESIDUOUS_NEEDLE_LEAF_FOREST = 3
        DESIDUOUS_BROAD_LEAF_FOREST = 4
        MIXED_FOREST = 5
        CLOSED_SHRUB_LANDS = 6
        OPEN_SHRUB_LANDS = 7
        WOODY_SAVANNAH = 8
        SAVANNAHS = 9
        GRASSLANDS = 10
        PERMANENT_WET_LANDS = 11
        CROP_LANDS = 12
        URBON_AND_BUILT_UP = 13
        CROPLAND_NATURAL_VEGETATION_MOSAIC = 14
        SNOW_AND_ICE = 15
        BARREN_OR_SPARSELY_VEGETATED = 16
        WATER_BODIES = 17

    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('land use map:\n' + str(self.map))


class ElevationMap:
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('elevation map:\n' + str(self.map))