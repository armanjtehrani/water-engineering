class Map:
    def __init__(self):
        self.n_cols = 0
        self.n_rows = 0
        self.xll_corner = 0
        self.yll_corner = 0
        self.cell_size = 0
        self.no_data_value = -9999
        self.matrix = []

    def set_config(self, another_map):
        """

        :type another_map: Map
        """
        self.n_cols = another_map.n_cols
        self.n_rows = another_map.n_rows
        self.xll_corner = another_map.xll_corner
        self.yll_corner = another_map.yll_corner
        self.cell_size = another_map.cell_size
        self.no_data_value = another_map.no_data_value

    def get_config_string(self):
        str_data = ""
        str_data += "ncols         " + str(self.n_cols) + '\n'
        str_data += "nrows         " + str(self.n_rows) + '\n'
        str_data += "xllcorner     " + str(self.xll_corner) + '\n'
        str_data += "yllcorner     " + str(self.yll_corner) + '\n'
        str_data += "cellsize      " + str(self.cell_size) + '\n'
        str_data += "NODATA_value  " + str(self.no_data_value) + '\n'
        return str_data

    def get_matrix_string(self):
        str_data = ""
        for row in self.matrix:
            for pixel in row:
                str_data += str(pixel) + ' '
            str_data += '\n'
        return str_data

    def __str__(self):
        str_data = self.get_config_string()
        str_data += "\n\n\nmap:\n"
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                str_data += str(self.matrix[i][j])
            str_data += '\n'
        return str_data

    def to_file(self, file_name, direc="map/"):
        file = open(direc + file_name, 'w+')
        str_data = ""
        str_data += self.get_config_string()
        str_data += self.get_matrix_string()
        file.write(str_data)

    def to_file_parammaps(self, file_name):
        file = open('parammaps/' + file_name, 'w+')
        str_data = ""
        str_data += self.get_config_string()
        str_data += self.get_matrix_string()
        file.write(str_data)

    def to_file_for_merge(self, file_name):
        file = open('usermaps/' + file_name, 'w+')
        str_data = ""
        str_data += self.get_config_string()
        str_data += self.get_matrix_string()
        file.write(str_data)


class GWMap:
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('ground water map:\n' + str(self.map))


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


class AdvancedLandUseMap:
    class VALUES:
        GREEN_ROOF = 20
        RAIN_GARDEN = 30
        RIPARIAN_ZONE = 40
        ROAD = 50

    VALUES_TO_NAMES = {
        VALUES.GREEN_ROOF: "flatroof",
        VALUES.RAIN_GARDEN: "raingarden",
        VALUES.RIPARIAN_ZONE: "riparianzone",
        VALUES.ROAD: "road",
    }

    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('advanced land use map:\n' + str(self.map))


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


class ParcelMap:
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('parcel map:\n' + str(self.map))


class SlopeMap:
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('slope map:\n' + str(self.map))


class DetailedLandUseMap:
    class VALUES:
        Asphalt = 2

    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('detailed landuse map:\n' + str(self.map))


class RunoffCoMap:
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('runoff coefficient map:\n' + str(self.map))


class FlowAccMap:
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('flow accumulator map:\n' + str(self.map))


class ConductivityMap:
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('conductivity map:\n' + str(self.map))


class BasicMap:
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('basic map:\n' + str(self.map))


class WaterShedMap:
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str('Watershed map:\n' + str(self.map))
