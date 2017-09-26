import time

from map_loader import MapLoader
from maps import Map
from maps import GWMap
from maps import SoilMap
from maps import LandUseMap
from maps import ParcelMap


map_loader = MapLoader()


class SuitableAreaBasedOnGW:
    def get_suitable_areas(self, GW_ascii_map_name, user_limit):
        self.gw_map = map_loader.load_map(GWMap, GW_ascii_map_name)
        self.output = Map()
        self.output.set_config(self.gw_map.map)
        # self.output.no_data_value = 0
        for i in range(len(self.gw_map.map.matrix)):
            self.output.matrix.append([])
            for pixel in self.gw_map.map.matrix[i]:
                if pixel == self.gw_map.map.no_data_value:
                    self.output.matrix[i].append(self.output.no_data_value)
                elif pixel > user_limit:
                    self.output.matrix[i].append(0)
                else:
                    self.output.matrix[i].append(1)
        return self.output


class SuitableSoilArea:
    def get_suitable_areas(self, soil_ascii_map_name, land_use_ascii_map_name, user_soil_number):
        self.soil_map = map_loader.load_map(SoilMap, soil_ascii_map_name)
        self.land_use_map = map_loader.load_map(LandUseMap, land_use_ascii_map_name)
        self.output = Map()
        self.output.set_config(self.soil_map.map)
        for i in range(len(self.soil_map.map.matrix)):
            self.output.matrix.append([])
            for j in range(len(self.soil_map.map.matrix[i])):
                if self.soil_map.map.matrix[i][j] == self.soil_map.map.no_data_value:
                    self.output.matrix[i].append(self.output.no_data_value)
                elif self.soil_map.map.matrix[i][j] != user_soil_number:
                    self.output.matrix[i].append(0)
                elif self.land_use_map.map.matrix[i][j] == LandUseMap.VALUES.URBON_AND_BUILT_UP or \
                        self.land_use_map.map.matrix[i][j] == LandUseMap.VALUES.WATER_BODIES:
                    self.output.matrix[i].append(0)
                else:
                    self.output.matrix[i].append(1)
        return self.output


class FindingRiperianZone:
    def __init__(self):
        self.land_use_map = LandUseMap()
        self.pixel_distance = 0
        self.output= Map()
        self.land_use_tuple = Map()

    def get_riperian_zone(self, land_use_ascii_map_name, user_distance):
        self.land_use_map = map_loader.load_map(LandUseMap, land_use_ascii_map_name)
        self.pixel_distance = user_distance / self.land_use_map.map.cell_size
        if int(self.pixel_distance) != self.pixel_distance:
            self.pixel_distance = int(self.pixel_distance) + 1
        self.pixel_distance = int(self.pixel_distance)
        self.output = Map()
        self.output.set_config(self.land_use_map.map)
        self.build_basic_output_matrix()
        landuse_map = self.land_use_map.map
        # t0 = time.time()
        for i in range(len(landuse_map.matrix)):
            for j in range(len(landuse_map.matrix[i])):
                if landuse_map.matrix[i][j] != landuse_map.no_data_value:
                    self.output.matrix[i][j] = 0
        for i in range(len(landuse_map.matrix)):
            for j in range(len(landuse_map.matrix[i])):
                if landuse_map.matrix[i][j] == LandUseMap.VALUES.WATER_BODIES:
                    self.highlight_nearby_pixels(i, j)
        # print('done:', time.time() - t0)
        return self.output

    def build_basic_output_matrix(self):
        self.output.matrix = [[self.output.no_data_value]*self.output.n_cols]*self.output.n_rows

    def highlight_nearby_pixels(self, i, j):
        landuse_map = self.land_use_map.map
        for x in range(i - self.pixel_distance, i + self.pixel_distance):
            for y in range(j - self.pixel_distance, j + self.pixel_distance):
                if landuse_map.matrix[x][y] != LandUseMap.VALUES.WATER_BODIES and \
                    landuse_map.matrix[x][y] != LandUseMap.VALUES.URBON_AND_BUILT_UP and \
                        landuse_map.matrix[x][y] != landuse_map.no_data_value:
                    self.output.matrix[x][y] = 1

    def get_riperian_zone2(self, land_use_ascii_map_name, user_distance):
        self.land_use_map = map_loader.load_map(LandUseMap, land_use_ascii_map_name)
        self.pixel_distance = user_distance / self.land_use_map.map.cell_size
        if int(self.pixel_distance) != self.pixel_distance:
            self.pixel_distance = int(self.pixel_distance) + 1
        self.pixel_distance = int(self.pixel_distance)
        self.output = Map()
        self.output.set_config(self.land_use_map.map)
        self.build_basic_output_matrix()
        landuse_map = self.land_use_map.map
        # t0 = time.time()
        for i in range(len(landuse_map.matrix)):
            for j in range(len(landuse_map.matrix[i])):
                if landuse_map.matrix[i][j] == landuse_map.no_data_value:
                    continue
                elif landuse_map.matrix[i][j] == LandUseMap.VALUES.WATER_BODIES or \
                    landuse_map.matrix[i][j] == LandUseMap.VALUES.URBON_AND_BUILT_UP:
                    self.output.matrix[i][j] = 0
                elif self.pixel_has_water_next_to_it(i, j):
                    self.output.matrix[i][j] = 1
                else:
                    self.output.matrix[i][j] = 0
        # print('done:', time.time() - t0)
        return self.output

    def build_basic_output_2(self):
        for i in range(len(self.land_use_map.map.matrix)):
            self.output.matrix.append([])
            for j in range(len(self.land_use_map.map.matrix[i])):
                self.output.matrix[i].append(self.output.no_data_value)

    def pixel_has_water_next_to_it(self, i, j):
        landuse_map = self.land_use_map.map
        for x in range(i - self.pixel_distance, i + self.pixel_distance):
            for y in range(j - self.pixel_distance, j + self.pixel_distance):
                if x == i and y == j:
                    continue
                if landuse_map.matrix[x][y] == LandUseMap.VALUES.WATER_BODIES:
                    return True
        return False


class RoofAreaFinder:
    def __init__(self):
        self.land_use_map = LandUseMap()
        self.parcel_map = ParcelMap()
        self.output = {}
        self.roof_pixels = {}

    def get_roof_areas(self, land_use_ascii_map_name, parcel_ascii_map_name):
        t0 = time.time()
        self.init_maps(land_use_ascii_map_name, parcel_ascii_map_name)
        for i in range(len(self.parcel_map.map.matrix)):
            for j in range(len(self.parcel_map.map.matrix[i])):
                if self.coordination_is_roof(i, j):
                    self.increase_roof_pixels(i, j)
        for key in self.roof_pixels.keys():
            self.output[key] = self.roof_pixels[key] * self.parcel_map.map.cell_size
        print(time.time() - t0)

        print('final data:', self.roof_pixels)
        print('final data:', self.output)


    def init_maps(self, land_use_ascii_map_name, parcel_ascii_map_name):
        self.land_use_map = map_loader.load_map(LandUseMap, land_use_ascii_map_name)
        self.parcel_map = map_loader.load_map(ParcelMap, parcel_ascii_map_name)
        self.output = {}
        self.roof_pixels = {}

    def coordination_is_roof(self, i, j):
        # try:
            # return self.land_use_map.map.matrix[i][j] == LandUseMap.VALUES.URBON_AND_BUILT_UP and \
               return self.parcel_map.map.matrix[i][j] != self.parcel_map.map.no_data_value
        # except:
        #     print('fuck')
        #     return False

    def increase_roof_pixels(self, i, j):
        roof_number = self.parcel_map.map.matrix[i][j]
        # print('roof number:', roof_number)
        num_of_pixels = self.roof_pixels.get(roof_number, 0)
        self.roof_pixels[roof_number] = num_of_pixels + 1
        # print('num of pixels:', num_of_pixels + 1)

# RoofAreaFinder().get_roof_areas('landuse.asc', 'roofs30.asc')
