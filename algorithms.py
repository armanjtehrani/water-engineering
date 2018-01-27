import copy
import os
import time

import maps
from map_loader import MapLoader
from maps import Map
from maps import GWMap
from maps import SoilMap
from maps import LandUseMap
from maps import ParcelMap
from maps import ElevationMap
from maps import DetailedLandUseMap
from maps import RunoffCoMap
from maps import AdvancedLandUseMap


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
        self.build_basic_output_2()
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


class RoofAreaCalculator:
    def __init__(self):
        self.land_use_map = LandUseMap()
        self.parcel_map = ParcelMap()
        self.output = {}
        self.roof_pixels = {}

    def get_roof_areas(self, land_use_ascii_map_name, parcel_ascii_map_name):
        self.init_maps(land_use_ascii_map_name, parcel_ascii_map_name)
        for i in range(len(self.parcel_map.map.matrix)):
            for j in range(len(self.parcel_map.map.matrix[i])):
                if self.coordination_is_roof(i, j):
                    self.increase_roof_pixels(i, j)
        for key in self.roof_pixels.keys():
            self.output[key] = self.roof_pixels[key] * self.parcel_map.map.cell_size
        return self.output

    def init_maps(self, land_use_ascii_map_name, parcel_ascii_map_name):
        self.land_use_map = map_loader.load_map(LandUseMap, land_use_ascii_map_name)
        self.parcel_map = map_loader.load_map(ParcelMap, parcel_ascii_map_name)
        self.output = {}
        self.roof_pixels = {}

    def coordination_is_roof(self, i, j):\
        return self.parcel_map.map.matrix[i][j] != self.parcel_map.map.no_data_value

    def increase_roof_pixels(self, i, j):
        roof_number = self.parcel_map.map.matrix[i][j]
        num_of_pixels = self.roof_pixels.get(roof_number, 0)
        self.roof_pixels[roof_number] = num_of_pixels + 1

    def build_map_for_output(self, file_name):
        file = open('maps/' + file_name, 'w+')
        str_data = ""
        str_data += self.parcel_map.map.get_config_string()
        str_data += str(self.output)
        file.write(str_data)


class FlatRoofFinder:
    def __init__(self):
        self.max_flat_roof_number = 0
        self.flat_roofs = Map()
        self.output = Map()
        self.land_use_map = LandUseMap()
        self.parcel_map = ParcelMap()
        self.dem_map = ElevationMap()
        self.minimum_valuable_area = 10
        self.maximum_possible_slope = 10
        self.roof_number_to_roofs = {}

    def get_flat_roofs_by_slope_map(self, land_use_ascii_map_name, parcel_ascii_map_name, slope_dot_map_name):
        pass

    def get_flat_roofs_by_elevation_map(self, land_use_ascii_map_name,
                                        parcel_ascii_map_name,
                                        dem_ascii_map_name,
                                        minimum_valuable_area,
                                        maximum_possible_slope):
        # t1 = time.time()
        self.init_variables_by_elevation_map(land_use_ascii_map_name,
                                             parcel_ascii_map_name,
                                             dem_ascii_map_name,
                                             minimum_valuable_area,
                                             maximum_possible_slope)
        # print('init:', time.time() - t1)
        # t2 = time.time()
        self.build_flat_roofs_map()
        # print('build:', time.time() - t2)
        # t3 = time.time()
        self.calculate_valuable_flat_roofs_by_area()
        # print('calculate:', time.time() - t3)
        return self.output

    def init_variables_by_elevation_map(self, land_use_ascii_map_name,
                                        parcel_ascii_map_name,
                                        dem_ascii_map_name,
                                        minimum_valuable_area,
                                        maximum_possible_slope):
        self.max_flat_roof_number = 0

        self.land_use_map = map_loader.load_map(LandUseMap, land_use_ascii_map_name)
        self.parcel_map= map_loader.load_map(ParcelMap, parcel_ascii_map_name)
        self.dem_map = map_loader.load_map(ElevationMap, dem_ascii_map_name)

        self.flat_roofs = Map()
        self.output = Map()
        self.flat_roofs.set_config(self.land_use_map.map)
        self.output.set_config(self.flat_roofs)
        for i in range(len(self.land_use_map.map.matrix)):
            self.flat_roofs.matrix.append([])
            self.output.matrix.append([])
            for j in range(len(self.land_use_map.map.matrix[i])):
                self.flat_roofs.matrix[i].append(self.flat_roofs.no_data_value)
                self.output.matrix[i].append(self.output.no_data_value)

        self.minimum_valuable_area = minimum_valuable_area
        self.maximum_possible_slope = maximum_possible_slope

        self.roof_number_to_roofs = {}

    def build_flat_roofs_map(self):
        landuse = self.land_use_map.map
        parcel = self.parcel_map.map
        for i in range(len(self.flat_roofs.matrix)):
            for j in range(len(self.flat_roofs.matrix[i])):
                if landuse.matrix[i][j] != LandUseMap.VALUES.URBON_AND_BUILT_UP or \
                        parcel.matrix[i][j] == parcel.no_data_value:
                    # if landuse.matrix[i][j] == LandUseMap.VALUES.URBON_AND_BUILT_UP or \
                    #         parcel.matrix[i][j] != parcel.no_data_value:
                    continue
                # pixel[i][j] is a roof
                # print('roof:)')
                # print('i:', i, 'j:', j)
                if self.flat_roofs.matrix[i][j] == self.flat_roofs.no_data_value:
                    # print('i am girvin:D')
                    self.set_new_number_for_roof(i, j)
                # else:
                #     print(self.flat_roofs.matrix[i][j])
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        # try:
                        #     print('x:', x, 'y:', y)
                        # except:
                        #     print('x o y out of index:D')
                        if x == i and y == j:
                            # print('khodam:D')
                            continue
                        if x < 0 or y < 0 or x >= self.flat_roofs.n_rows or y >= self.flat_roofs.n_cols:
                            # print('roof on gooshe:D')
                            continue
                        # now pixel[x][y] exist!
                        if landuse.matrix[x][y] != LandUseMap.VALUES.URBON_AND_BUILT_UP or \
                                parcel.matrix[x][y] == parcel.no_data_value:
                            # print('edge roof:D')
                            continue
                        # now pixel[x][y] is a roof
                        if not self.pixels_are_in_the_same_range(i, j, x, y):
                            # print('near roof not in same range')
                            continue
                        # now pixel[i][j] and pixel[x][y] are next to each other and are flat
                        if self.flat_roofs.matrix[x][y] == self.flat_roofs.matrix[i][j]:
                            # print('all the same chib:D')
                            continue
                        if self.flat_roofs.matrix[x][y] == self.flat_roofs.no_data_value:
                            # print('new near girvin roof:D')
                            self.set_new_pixel_with_new_range(x, y, i, j)
                        else:
                            # print('chib roof:D')
                            self.set_all_pixels_in_new_range_with_ones_in_old_range(i, j, x, y)
                # os.system('pause')

    def set_new_number_for_roof(self, i, j):
        self.max_flat_roof_number += 1
        self.roof_number_to_roofs[self.max_flat_roof_number] = []
        self.roof_number_to_roofs[self.max_flat_roof_number].append({'x': i, 'y': j})
        self.flat_roofs.matrix[i][j] = self.max_flat_roof_number

    def pixels_are_in_the_same_range(self, i, j, x, y):
        if abs(self.dem_map.map.matrix[i][j] - self.dem_map.map.matrix[x][y]) < self.maximum_possible_slope:
            return True
        return False

    def set_new_pixel_with_new_range(self, x, y, i, j):
        # print('old girvin:', self.flat_roofs.matrix[x][y])
        self.flat_roofs.matrix[x][y] = self.flat_roofs.matrix[i][j]
        # print('new chib:D:', self.flat_roofs.matrix[x][y])
        # print('old roof:', self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]])
        self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]].append({'x': x, 'y': y})
        # print('new roof:', self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]])

    def set_all_pixels_in_new_range_with_ones_in_old_range(self, i, j, x, y):
        roof_number_that_should_be_deleted = self.flat_roofs.matrix[i][j]
        # print('deleted roof number:', roof_number_that_should_be_deleted)
        main_roof_number = self.flat_roofs.matrix[x][y]
        # print('main roof number:', main_roof_number)
        roofs_that_should_go_to_main_roof_number = self.roof_number_to_roofs[roof_number_that_should_be_deleted]
        # print('ed up roofs:', roofs_that_shoud_go_to_main_roof_number)
        # print('main roofs before:', self.roof_number_to_roofs[main_roof_number])
        for roof in roofs_that_should_go_to_main_roof_number:
            self.flat_roofs.matrix[roof['x']][roof['y']] = main_roof_number
            self.roof_number_to_roofs[main_roof_number].append(roof)
        # print('main roofs after:', self.roof_number_to_roofs[main_roof_number])
        self.roof_number_to_roofs[roof_number_that_should_be_deleted] = []
        # print('ed up number:', self.roof_number_to_roofs[roof_number_that_should_be_deleted])

    def calculate_valuable_flat_roofs_by_area(self):
        minimum_pixels_to_be_useful = self.minimum_valuable_area / (self.output.cell_size ** 2)
        # print('num:', minimum_pixels_to_be_useful)
        # t = 0
        # i = 0
        # for key in self.roof_number_to_roofs:
        #     # print(len(self.roof_number_to_roofs[key]))
        #     if len(self.roof_number_to_roofs[key]) > 0:
        #         # print('t yes')
        #         t += 1
        #     if len(self.roof_number_to_roofs[key]) >= minimum_pixels_to_be_useful:
        #         # print('i yes')
        #         i += 1
        # print('t:', t)
        # print('i:', i)
        tmp_number_to_roof = copy.deepcopy(self.roof_number_to_roofs)
        for key in self.roof_number_to_roofs:
            # print('flat roof number', key, ':')
            # print(self.roof_number_to_roofs[key])
            # print('len is:', len(self.roof_number_to_roofs[key]))
            if len(self.roof_number_to_roofs[key]) < minimum_pixels_to_be_useful:
                del tmp_number_to_roof[key]  # not so sure about it!
                continue
            # flat roof size is good
            # print(key, 'added:)')
            for roof in self.roof_number_to_roofs[key]:
                # print('before output number i:', roof['x'], 'j:', roof['y'], 'was: ', self.output.matrix[roof['x']][roof['y']])
                self.output.matrix[roof['x']][roof['y']] = key
                # print('now output number i:', roof['x'], 'j:', roof['y'], 'is: ', self.output.matrix[roof['x']][roof['y']])
            # os.system('pause')
        self.roof_number_to_roofs = tmp_number_to_roof


class RoadFinder :
    def __init__(self):
        self.detailed_landuse_map = DetailedLandUseMap()
        self.output = Map()

    def get_detailed_landuse_map(self, detailed_landuse_map_ascii):
        self.detailed_landuse_map = map_loader.load_map(DetailedLandUseMap, detailed_landuse_map_ascii)
        detailed_landuse_map = self.detailed_landuse_map.map
        self.build_basic_output()
        for i in range(len(detailed_landuse_map.matrix)):
            for j in range(len(detailed_landuse_map.matrix[i])):
                if detailed_landuse_map.matrix[i][j] == detailed_landuse_map.no_data_value:
                    continue
                if detailed_landuse_map.mطططططططatrix[i][j] == DetailedLandUseMap.VALUES.Asphalt:
                    self.output.matrix[i][j] = 1
                else:
                    self.output.matrix[i][j] = 0
        return self.output

    def build_basic_output(self):
        for i in range(len(self.detailed_landuse_map.map.matrix)):
            self.output.matrix.append([])
            for j in range(len(self.detailed_landuse_map.map.matrix[i])):
                self.output.matrix[i].append(self.output.no_data_value)


class RunoffCoefficient:
    def __init__(self):
        self.runoff_coefficient_map = RunoffCoMap()
        self.output = Map()

    def get_runoff_coefficient_map(self, runoff_coefficient_map_ascii, user_limit):
        self.runoff_coefficient_map = map_loader.load_map(RunoffCoefficient, runoff_coefficient_map_ascii)
        runoff_coefficient_map = self.runoff_coefficient_map.map
        self.build_basic_output()
        for i in range(len(runoff_coefficient_map.matrix)):
            for j in range(len(runoff_coefficient_map.matrix[i])):
                if runoff_coefficient_map.matrix[i][j] == runoff_coefficient_map.no_data_value:
                    if runoff_coefficient_map.matrix[i][j] >= user_limit:
                        self.output.matrix[i][j] = 1
                    else:
                        self.output.matrix[i][j] = 0
        return self.output

    def build_basic_output(self):
        for i in range(len(self.runoff_coefficient_map.map.matrix)):
            self.output.matrix.append([])
            for j in range(len(self.runoff_coefficient_map.map.matrix[i])):
                self.output.matrix[i].append(self.output.no_data_value)


class RainGardenFinder:
    def __init__(self):
        self.list_of_acceptable_land_use_parts = [
            LandUseMap.VALUES.URBON_AND_BUILT_UP,
            LandUseMap.VALUES.WATER_BODIES
        ]

        self.max_rain_garden_id = 0
        self.rain_gardens = Map()
        self.output = Map()
        self.land_use_map = LandUseMap()
        self.minimum_valuable_area = 10
        self.rain_garden_ids_to_pixels = {}

    def get_rain_gardens(self, land_use_ascii_map_name, minimum_valuable_area):
        # t1 = time.time()
        self.init_variables(land_use_ascii_map_name, minimum_valuable_area)
        # print('init:', time.time() - t1)
        # t2 = time.time()
        self.build_rain_garden_map()
        # print('build:', time.time() - t2)
        # t3 = time.time()
        self.calculate_valuable_rain_gardens_by_area()
        # print('calculate:', time.time() - t3)
        return self.output

    def init_variables(self, land_use_ascii_map_name, minimum_valuable_area):
        self.max_rain_garden_id = 0

        self.land_use_map = map_loader.load_map(LandUseMap, land_use_ascii_map_name)
        self.rain_gardens = Map()
        self.output = Map()
        self.rain_gardens.set_config(self.land_use_map.map)
        self.output.set_config(self.rain_gardens)
        for i in range(len(self.land_use_map.map.matrix)):
            self.rain_gardens.matrix.append([])
            self.output.matrix.append([])
            for j in range(len(self.land_use_map.map.matrix[i])):
                self.rain_gardens.matrix[i].append(self.rain_gardens.no_data_value)
                self.output.matrix[i].append(self.output.no_data_value)

        self.minimum_valuable_area = minimum_valuable_area

        self.rain_garden_ids_to_pixels = {}

    def build_rain_garden_map(self):
        landuse = self.land_use_map.map
        for i in range(len(self.rain_gardens.matrix)):
            for j in range(len(self.rain_gardens.matrix[i])):
                if landuse.matrix[i][j] == landuse.no_data_value:
                    continue
                if landuse.matrix[i][j] not in self.list_of_acceptable_land_use_parts:
                    self.rain_gardens.matrix[i][j] = 0
                    continue
                # pixel[i][j] is a roof
                # print('roof:)')
                # print('i:', i, 'j:', j)
                if self.rain_gardens.matrix[i][j] == self.rain_gardens.no_data_value:
                    # print('i am girvin:D')
                    self.set_new_id_for_garden(i, j)
                # else:
                #     print(self.flat_roofs.matrix[i][j])
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        # try:
                        #     print('x:', x, 'y:', y)
                        # except:
                        #     print('x o y out of index:D')
                        if x == i and y == j:
                            # print('khodam:D')
                            continue
                        if x < 0 or y < 0 or x >= self.rain_gardens.n_rows or y >= self.rain_gardens.n_cols:
                            # print('roof on gooshe:D')
                            continue
                        # now pixel[x][y] exist!
                        if landuse.matrix[x][y] not in self.list_of_acceptable_land_use_parts:
                            # print('edge roof:D')
                            continue
                        # now pixel[x][y] is a rain garden
                        if self.rain_gardens.matrix[x][y] == self.rain_gardens.matrix[i][j]:
                            # print('all the same chib:D')
                            continue
                        if self.rain_gardens.matrix[x][y] == self.rain_gardens.no_data_value:
                            # print('new near girvin roof:D')
                            self.set_new_pixel_with_new_range(x, y, i, j)
                        else:
                            # print('chib roof:D')
                            self.set_all_pixels_in_new_range_with_ones_in_old_range(i, j, x, y)
                # os.system('pause')

    def set_new_id_for_garden(self, i, j):
        self.max_rain_garden_id += 1
        self.rain_gardens.matrix[i][j] = self.max_rain_garden_id
        self.rain_garden_ids_to_pixels[self.max_rain_garden_id] = []
        self.rain_garden_ids_to_pixels[self.max_rain_garden_id].append({'x': i, 'y': j})

    def set_new_pixel_with_new_range(self, x, y, i, j):
        # print('old girvin:', self.flat_roofs.matrix[x][y])
        self.rain_gardens.matrix[x][y] = self.rain_gardens.matrix[i][j]
        # print('new chib:D:', self.flat_roofs.matrix[x][y])
        # print('old roof:', self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]])
        self.rain_garden_ids_to_pixels[self.rain_gardens.matrix[x][y]].append({'x': x, 'y': y})
        # print('new roof:', self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]])

    def set_all_pixels_in_new_range_with_ones_in_old_range(self, i, j, x, y):
        rain_garden_number_that_should_be_deleted = self.rain_gardens.matrix[i][j]
        # print('deleted roof number:', roof_number_that_should_be_deleted)
        main_rain_garden_number = self.rain_gardens.matrix[x][y]
        # print('main roof number:', main_roof_number)
        rain_gardens_that_should_go_to_main_rain_garden_id = \
            self.rain_garden_ids_to_pixels[rain_garden_number_that_should_be_deleted]
        # print('ed up roofs:', roofs_that_shoud_go_to_main_roof_number)
        # print('main roofs before:', self.roof_number_to_roofs[main_roof_number])
        for rain_garden in rain_gardens_that_should_go_to_main_rain_garden_id:
            self.rain_gardens.matrix[rain_garden['x']][rain_garden['y']] = main_rain_garden_number
            self.rain_garden_ids_to_pixels[main_rain_garden_number].append(rain_garden)
        # print('main roofs after:', self.roof_number_to_roofs[main_roof_number])
        self.rain_garden_ids_to_pixels[rain_garden_number_that_should_be_deleted] = []
        # print('ed up number:', self.roof_number_to_roofs[roof_number_that_should_be_deleted])

    def calculate_valuable_rain_gardens_by_area(self):
        minimum_pixels_to_be_useful = self.minimum_valuable_area / (self.output.cell_size ** 2)
        # print('num:', minimum_pixels_to_be_useful)
        # t = 0
        # i = 0
        # for key in self.roof_number_to_roofs:
        #     # print(len(self.roof_number_to_roofs[key]))
        #     if len(self.roof_number_to_roofs[key]) > 0:
        #         # print('t yes')
        #         t += 1
        #     if len(self.roof_number_to_roofs[key]) >= minimum_pixels_to_be_useful:
        #         # print('i yes')
        #         i += 1
        # print('t:', t)
        # print('i:', i)
        tmp_ids_to_pixels = copy.deepcopy(self.rain_garden_ids_to_pixels)
        for key in self.rain_garden_ids_to_pixels:
            # print('flat roof number', key, ':')
            # print(self.roof_number_to_roofs[key])
            # print('len is:', len(self.roof_number_to_roofs[key]))
            if len(self.rain_garden_ids_to_pixels[key]) < minimum_pixels_to_be_useful:
                del tmp_ids_to_pixels[key]    # not so sure about it!
                continue
            # flat roof size is good
            # print(key, 'added:)')
            for rain_garden in self.rain_garden_ids_to_pixels[key]:
                # print('before output number i:', roof['x'], 'j:', roof['y'], 'was: ', self.output.matrix[roof['x']][roof['y']])
                self.output.matrix[rain_garden['x']][rain_garden['y']] = key
                # print('now output number i:', roof['x'], 'j:', roof['y'], 'is: ', self.output.matrix[roof['x']][roof['y']])
            # os.system('pause')
        self.rain_garden_ids_to_pixels = tmp_ids_to_pixels


class ChooseStuff:
    temp_list = []
    final_list = {}

    def choose_m_from_n(self, n, m, from_=0):
        if from_ > n:
            return
        for i in range(from_, n - m + 1):
            self.temp_list.append(i)
            # print('from:', from_, 'to:', n-m+1)
            if m > 1:
                self.choose_m_from_n(n, m - 1, i+1)
            else:
                length = len(self.temp_list)
                if self.final_list.get(length) is None:
                    self.final_list[length] = []
                self.final_list[length].append(copy.deepcopy(self.temp_list))
                # print(self.temp_list)
            self.temp_list.pop(-1)
        # print('fucked:', n-m-1)


    def choose_all_situations_of_n(self, n):
        self.temp_list = []
        self.final_list = {}
        t1 = time.time()
        for m in range(1, n + 1):
            print('choosing m:', m)
            t = time.time()
            self.choose_m_from_n(n, m)
            print(time.time() - t)
        print('final time:', time.time() - t1)
        return self.final_list


class UserMergeForAlgorithms:
    def __init__(self):
        self.user_limit_on_max_maps_per_percent = 0
        self.priority_list = None
        self.num_of_pixels_of_priority = None
        self.priority_index = 0
        self.priority_item = None
        self.basic_landuse_map = None
        self.advanced_landuse_map = None
        # self.my_map = None
        self.parcel_map = None
        self.dem_map = None
        self.priority_maps = None

        # cleaner version
        self.basic_map_for_new_priority = None

    # input
    LANDUSE_NAME = 'land_use_ascii_map_name'
    MIN_AREA = 'minimum_valuable_area'
    PARCEL_NAME = 'parcel_ascii_map_name'
    DEM_NAME = 'dem_ascii_map_name'
    MAX_SLOPE = 'max_possible_slope_for_flat_roof'

    # consts
    STEP = 5

    chooser = ChooseStuff()

    def calculate_rain_garden_table(self):
        self.build_rain_garden_ids_to_pixels()
        self.priority_item = AdvancedLandUseMap.VALUES.RAIN_GARDEN
        self.rain_garden_percent_to_ids = self.calculate_descrit_table(self.rain_garden_ids_to_pixels)
        # format:
        # {'5':[[1,2,3], [4,5,6,]],
        # '10':[[1,2,3,4,5,6], [7,8,9,10,11,12]],
        # ...}

    def build_rain_garden_ids_to_pixels(self):
        my_rain_garden_finder = RainGardenFinder()
        rain_garden_output = my_rain_garden_finder.get_rain_gardens(
            self.rain_garden_need[self.LANDUSE_NAME],
            self.rain_garden_need[self.MIN_AREA])
        self.rain_garden_ids_to_pixels = my_rain_garden_finder.rain_garden_ids_to_pixels

    def calculate_green_roof_table(self):
        self.build_flat_roof_ids_to_pixels()
        print('built flat roof ids to pixels')
        self.priority_item = AdvancedLandUseMap.VALUES.GREEN_ROOF
        self.flat_roof_percent_to_ids = self.calculate_descrit_table(self.flat_roof_ids_to_pixels)
        # format:
        # {'5':[[1,2,3], [4,5,6,]],
        # '10':[[1,2,3,4,5,6], [7,8,9,10,11,12]],
        # ...}

    def build_flat_roof_ids_to_pixels(self):
        my_flat_roof_finder = FlatRoofFinder()
        flat_roof_output = my_flat_roof_finder.get_flat_roofs_by_elevation_map(
            self.flat_roof_need[self.LANDUSE_NAME],
            self.flat_roof_need[self.PARCEL_NAME],
            self.flat_roof_need[self.DEM_NAME],
            self.flat_roof_need[self.MIN_AREA],
            self.flat_roof_need[self.MAX_SLOPE])
        self.flat_roof_ids_to_pixels = my_flat_roof_finder.roof_number_to_roofs

    def calculate_smallest_num_of_pixels(self, ids_to_pixels):
        smallest = 100000000
        for i in ids_to_pixels:
            if len(ids_to_pixels[i]) < smallest:
                smallest = len(ids_to_pixels[i])
                print('small:', smallest)
        print('final smallest:', smallest)
        return smallest

    def calculate_descrit_table(self, ids_to_pixels):
        print('calculate descrit table')
        max_len = int(100/self.STEP)
        table = {}
        for len in range(1, max_len + 1):   # for percents
            percent = len * self.STEP
            print('percent:', percent)
            print('priority item:', self.priority_item)
            all_priority_pixels = self.num_of_pixels_of_priority[self.priority_item]
            print('all pixs:', all_priority_pixels)
            max_num_of_pixels = int(all_priority_pixels * percent/100)
            print('max num of pixels:', max_num_of_pixels)
            ids_for_this_percent = self.calc(ids_to_pixels, max_num_of_pixels)
            table[percent] = ids_for_this_percent
        return table

    def calc(self, ids_to_pixels, max_num_of_pixels):
        print('in calc:')
        ids_list_for_percent = []
        while True:
            print('new True')
            max_no = max_num_of_pixels
            new_list_of_ids_for_percent = []
            smallest_num_of_pixels = self.calculate_smallest_num_of_pixels(ids_to_pixels)
            if smallest_num_of_pixels > max_no:
                print('11111111111')
                break
            if not ids_to_pixels:
                print('22222222222')
                break
            tmp_rain_garden_ids_to_pixels = copy.deepcopy(ids_to_pixels)
            for _id in ids_to_pixels:
                num_of_pixels = len(ids_to_pixels[_id])
                if num_of_pixels > max_no:
                    print('left it::::::::::num:', num_of_pixels, ', max:', max_no)
                    continue
                max_no -= num_of_pixels
                print('max num', max_no)
                new_list_of_ids_for_percent.append(_id)
                # print('map111:', new_map_pixels[rain_id])
                del tmp_rain_garden_ids_to_pixels[_id]
                print('deleted the bech', len(tmp_rain_garden_ids_to_pixels), len(ids_to_pixels))
                # print('map222:', new_map_pixels[rain_id])
            print('new max:', max_no)
            ids_to_pixels = tmp_rain_garden_ids_to_pixels
            print('new ids to pixels:', len(ids_to_pixels))
            if new_list_of_ids_for_percent:
                ids_list_for_percent.append(new_list_of_ids_for_percent)
        return ids_list_for_percent

    def init_in_clean_way(self, priority_list, basic_landuse_map, advanced_landuse_map,
                          user_limit_on_max_maps_per_percent,
                          things_needed_for_rain_garden_calculation,
                          things_needed_for_flat_roof_calculation):
        print('in init in clean way')

        self.user_limit_on_max_maps_per_percent = user_limit_on_max_maps_per_percent
        self.priority_list = priority_list

        # build self.priority_maps format & calculate number of pixels for each priority map
        self.num_of_pixels_of_priority = {}
        self.priority_maps = {}
        for priority_name in priority_list:
            self.num_of_pixels_of_priority[priority_name] = 0
            self.priority_maps[priority_name] = {'maps': {}, 'final': None}
        matrix = advanced_landuse_map.map.matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                data = int(matrix[i][j])
                if data in priority_list:
                    self.num_of_pixels_of_priority[data] += 1
        print('final pixel nums:', self.num_of_pixels_of_priority)

        # basic priority maps format:
        # priority_maps = {
        #     priority_item: {
        #     'priority': 0,
        #     'final': Map(),
        #     'maps': {
        #         5:[Map1, Map2, ...],
        #         10:[Map1, Map2, ...],
        #         ...,
        #         100:[Map1]
        #     }
        # }
        # }
        self.basic_landuse_map = basic_landuse_map
        # my_map in init
        self.advanced_landuse_map = advanced_landuse_map

        ### final map for previous priority -> basic map for new priority
        ### basic map for first priority -> basic landuse map!
        self.basic_map_for_new_priority = self.basic_landuse_map.map

        self.rain_garden_need = things_needed_for_rain_garden_calculation
        if AdvancedLandUseMap.VALUES.RAIN_GARDEN in priority_list:
            self.check_if_rain_garden_needed_stuff_are_right()
            print('go in calculate rain garden table')
            self.calculate_rain_garden_table()
        self.flat_roof_need = things_needed_for_flat_roof_calculation
        if AdvancedLandUseMap.VALUES.GREEN_ROOF in priority_list:
            self.check_if_flat_roof_needed_stuff_are_right()
            print('go in calculate green roof table')
            self.calculate_green_roof_table()

    def check_if_rain_garden_needed_stuff_are_right(self):
        if self.rain_garden_need.get(self.LANDUSE_NAME) is None:
            raise("landuse ascii map not included for rain garden in UserMergeForAlgorithms class. please include it")
        if self.rain_garden_need.get(self.MIN_AREA) is None:
            raise("minimum rain garden valuable area is not included for rain garden in UserMergeForAlgorithms class. "
                  "please include it")
        try:
            self.rain_garden_need[self.MIN_AREA] = int(self.rain_garden_need[self.MIN_AREA])
        except:
            raise ("minimum rain garden valuable area type is not int. it is " +
                   str(type(self.rain_garden_need[self.MIN_AREA])))

    def check_if_flat_roof_needed_stuff_are_right(self):
        if self.flat_roof_need.get(self.LANDUSE_NAME) is None:
            raise ("landuse ascii map not included for flat roof in UserMergeForAlgorithms class. please include it")
        if self.flat_roof_need.get(self.PARCEL_NAME) is None:
            raise ("parcel ascii map not included for flat roof in UserMergeForAlgorithms class. please include it")
        if self.flat_roof_need.get(self.DEM_NAME) is None:
            raise ("dem ascii map not included for flat roof in UserMergeForAlgorithms class. please include it")
        if self.flat_roof_need.get(self.MIN_AREA) is None:
            raise("minimum flat roof valuable area is not included for flat roof in UserMergeForAlgorithms class. "
                  "please include it")
        try:
            self.flat_roof_need[self.MIN_AREA] = int(self.flat_roof_need[self.MIN_AREA])
        except:
            raise ("minimum flat roof valuable area type is not int. it is " +
                   str(type(self.flat_roof_need[self.MIN_AREA])))
        if self.flat_roof_need.get(self.MAX_SLOPE) is None:
            raise("maximum possible slope is not included for flat roof in UserMergeForAlgorithms class. "
                  "please include it")
        try:
            self.flat_roof_need[self.MAX_SLOPE] = int(self.flat_roof_need[self.MAX_SLOPE])
        except:
            raise ("maximum possible slope for flat roof type is not int. it is " +
                   str(type(self.flat_roof_need[self.MAX_SLOPE])))


    # def init(self, priority_list, basic_landuse_map, advanced_landuse_map,
    #          basic_landuse_ascii_map_name_for_rain_garden_and_flat_roof, minimum_rain_garden_valuable_area,
    #          parcel_ascii_map_name_for_flat_roof, dem_ascii_map_name_for_flat_roof, minimum_flat_roof_valuable_area,
    #          maximum_possible_slope_for_flat_roof,
    #          user_limit_on_max_maps_per_percent):
    #     #   raingarden
    #     self.basic_landuse_ascii_map_name_for_rain_garden_and_flat_roof = basic_landuse_ascii_map_name_for_rain_garden_and_flat_roof
    #     self.minimum_rain_garden_valuable_area = minimum_rain_garden_valuable_area
    #
    #     #   flat roof
    #     self.parcel_ascii_map_name_for_flat_roof = parcel_ascii_map_name_for_flat_roof
    #     self.dem_ascii_map_name_for_flat_roof = dem_ascii_map_name_for_flat_roof
    #     self.minimum_flat_roof_valuable_area = minimum_flat_roof_valuable_area
    #     self.maximum_possible_slope_for_flat_roof = maximum_possible_slope_for_flat_roof
    #
    #     self.user_limit_on_max_maps_per_percent = user_limit_on_max_maps_per_percent
    #     self.priority_list = priority_list
    #     self.num_of_pixels_of_priority = {}
    #     self.priority_maps = {}
    #     for priority_name in priority_list:
    #         self.num_of_pixels_of_priority[priority_name] = 0
    #         self.priority_maps[priority_name] = {'maps': {}, 'final': None}
    #     matrix = advanced_landuse_map.map.matrix
    #     for i in range(len(matrix)):
    #         for j in range(len(matrix)):
    #             data = int(matrix[i][j])
    #             if data in priority_list:
    #                 self.num_of_pixels_of_priority[data] += 1
    #     print('final pixel nums:', self.num_of_pixels_of_priority)
    #         # priority maps:{
    #         #     priority item: {
    #         #     'final': Map(),
    #         #     'maps': {
    #         #         5:[Map1, Map2, ...],
    #         #         10:[Map1, Map2, ...],
    #         #         ...,
    #         #         100:[Map1]
    #         #     }
    #         # }
    #         # }
    #     self.basic_landuse_map = basic_landuse_map
    #     self.advanced_landuse_map = advanced_landuse_map
    #     self.my_map = advanced_landuse_map
    #
    #     ### old final maps, new basic maps
    #     self.basic_map_for_me = self.basic_landuse_map.map.matrix

    # def get_priorities(self, priority_list, basic_landuse_map, advanced_landuse_map,
    #                    basic_landuse_ascii_map_name_for_rain_garden_and_flat_roof, minimum_rain_garden_valuable_area,
    #                    parcel_ascii_map_name_for_flat_roof, dem_ascii_map_name_for_flat_roof, minimum_flat_roof_valuable_area, maximum_possible_slope_for_flat_roof,
    #                    user_limit_on_max_maps_per_percent):    # main method
    #     print('first. priority list:', priority_list)
    #     self.init(priority_list, basic_landuse_map, advanced_landuse_map,
    #               basic_landuse_ascii_map_name_for_rain_garden_and_flat_roof, minimum_rain_garden_valuable_area,
    #               parcel_ascii_map_name_for_flat_roof, dem_ascii_map_name_for_flat_roof, minimum_flat_roof_valuable_area, maximum_possible_slope_for_flat_roof,
    #               user_limit_on_max_maps_per_percent)
    #     print('after basic init')
    #     self.print()
    #     for priority_index in range(len(priority_list)):
    #         print('on priority index:', priority_index)
    #         self.priority_index = priority_index
    #         self.priority_item = priority_list[priority_index]
    #         print('on priority item:', self.priority_item)
    #         self.build_maps_for_priority_item()
    #     return self.priority_maps

    # ***************main method***************
    def get_priorities_in_clean_way(self, priority_list, basic_landuse_map, advanced_landuse_map,
                                    user_limit_on_max_map_per_percent,
                                    things_needed_for_rain_garden_calculation,
                                    things_needed_for_flat_roof_calculation):
        print('start\npriority list:', priority_list)
        self.init_in_clean_way(priority_list, basic_landuse_map, advanced_landuse_map,
                               user_limit_on_max_map_per_percent,
                               things_needed_for_rain_garden_calculation,
                               things_needed_for_flat_roof_calculation)
        print('after basic init')
        self.print()
        for priority_index in range(len(priority_list)):
            self.priority_index = priority_index
            self.priority_item = priority_list[priority_index]
            print('on priority index:', self.priority_index)
            print('on priority item:', self.priority_item)
            self.build_maps_for_priority_item_in_clean_way()
        return self.priority_maps

    def print(self):
        print('****************inside print***************')
        print('priority list:', self.priority_list)
        print('priority maps:', self.priority_maps)
            # priority maps:{
            #     priority item: {
            #     'priority': 0,
            #     'final': Map(),
            #     'maps': {
            #         5:[Map1, Map2, ...],
            #         10:[Map1, Map2, ...],
            #         ...,
            #         100:[Map1]
            #     }
            # }
            # }

    def build_maps_for_priority_item_in_clean_way(self):
        all_maps_for_1_priority = {'maps': {}, 'final': None, 'priority': self.priority_index}
        print('start for priority:')
        if self.priority_item == AdvancedLandUseMap.VALUES.GREEN_ROOF:
            print('green roof')
            method_to_call_for_priority_item = self.build_green_roof_maps_for_priority_item_with_percentage_in_clean_way
        elif self.priority_item == AdvancedLandUseMap.VALUES.RAIN_GARDEN:
            print('rain garden')
            method_to_call_for_priority_item = \
                self.build_rain_garden_maps_for_priority_item_with_percentage_in_clean_way
        else:
            print('continuous')
            method_to_call_for_priority_item = self.build_continuous_maps_for_priority_item_with_percentage
        all_priority_pixels = self.num_of_pixels_of_priority[self.priority_item]
        biggest_len = int(100 / self.STEP)
        for i in range(1, biggest_len + 1):
            print('len:', i)
            percent = self.STEP * i
            print('%:', percent)
            num_of_pixels = int(all_priority_pixels * (percent / 100))
            print('all of pixels:', all_priority_pixels)
            print('num of pixels:', num_of_pixels)
            all_maps_in_specific_percent = method_to_call_for_priority_item(num_of_pixels, percent)
            print('maps len:', len(all_maps_in_specific_percent))
            all_maps_for_1_priority['maps'][percent] = all_maps_in_specific_percent
            next_percent = percent + self.STEP
            if next_percent > 100:
                all_maps_for_1_priority['final'] = all_maps_in_specific_percent[0]  # should not be empty!!
                self.basic_map_for_new_priority = all_maps_for_1_priority['final']
                # print('maps for priority:', maps_for_priority)
        self.priority_maps[self.priority_item] = all_maps_for_1_priority
        print('final priority maps:', len(self.priority_maps[self.priority_item]))

    # def build_maps_for_priority_item(self):
    #     step = 5
    #     maps_for_priority = {'maps': {}, 'final': None}
    #     print('start:')
    #     if self.priority_item == AdvancedLandUseMap.VALUES.GREEN_ROOF:
    #         print('green roof')
    #         method_to_call_for_priority_item = self.build_green_roof_maps_for_priority_item_with_percentage
    #     elif self.priority_item == AdvancedLandUseMap.VALUES.RAIN_GARDEN:
    #         print('rain garden')
    #         method_to_call_for_priority_item = self.build_rain_garden_maps_for_priority_item_with_percentage
    #     else:
    #         print('continuous')
    #         method_to_call_for_priority_item = self.build_continuous_maps_for_priority_item_with_percentage
    #     all_priority_pixels = self.num_of_pixels_of_priority[self.priority_item]
    #     for i in range(1, int(100 / step) + 1):
    #         print('i:', i)
    #         percent = step * i
    #         print('%:', percent)
    #         num_of_pixels = int(all_priority_pixels * (percent/100))
    #         print('alllll of pixels:', all_priority_pixels)
    #         print('num of pixels:', num_of_pixels)
    #         maps = [[]]
    #         maps = method_to_call_for_priority_item(num_of_pixels)
    #         print('maps len:', len(maps))
    #         maps_for_priority['maps'][percent] = maps
    #         if percent == 100:
    #             maps_for_priority['final'] = maps[0]  # should not be empty!!
    #             self.basic_map_for_me = maps_for_priority['final']
    #         # print('maps for priority:', maps_for_priority)
    #     self.priority_maps[self.priority_item] = maps_for_priority
    #     print('final priority maps:', len(self.priority_maps[self.priority_item]))

    def build_green_roof_maps_for_priority_item_with_percentage_in_clean_way(self, num_of_pixels, percent):
        print('in build green roof for percent:', percent)
        maps = self.build_descrit_maps_with_percent_to_id_from_calc_method(
            percent,
            self.flat_roof_percent_to_ids,
            self.flat_roof_ids_to_pixels,
            AdvancedLandUseMap.VALUES.GREEN_ROOF)
        print('ret maps:', maps)
        return maps

    def build_rain_garden_maps_for_priority_item_with_percentage_in_clean_way(self, num_of_pixels, percent):
        print('in build rain garden for percent:', percent)
        maps = self.build_descrit_maps_with_percent_to_id_from_calc_method(
            percent,
            self.rain_garden_percent_to_ids,
            self.rain_garden_ids_to_pixels,
            AdvancedLandUseMap.VALUES.RAIN_GARDEN)
        print('ret maps:', maps)
        return maps

    def build_descrit_maps_with_percent_to_id_from_calc_method(self, percent, percent_to_ids, ids_to_pixels, value):
        ids_for_percent = percent_to_ids[percent]
        print('ids->percent', ids_for_percent)
        maps = []

        for ids in ids_for_percent:
            map = copy.deepcopy(self.basic_map_for_new_priority)
            print('ids:', ids)
            for id_ in ids:
                # print('id_', id_)
                # print('ids_', ids)
                # print('type:', type(ids_to_pixels))
                # print('data:', ids_to_pixels)
                for pixel in ids_to_pixels[id_]:
                    # print('x:', pixel['x'])
                    # print('y:', pixel['y'])
                    # print('matrix:', map.matrix[pixel['x']])
                    map.matrix[pixel['x']][pixel['y']] = value
            maps.append(map)
            if len(maps) >= self.user_limit_on_max_maps_per_percent:
                print('reached user limit!')
                return maps
        return maps

    # def build_green_roof_maps_for_priority_item_with_percentage(self, max_num_of_pixels):
    #     new_maps = []
    #     print('green roof2')
    #     my_flat_roof_finder = FlatRoofFinder()
    #     flat_roof_output = my_flat_roof_finder.get_flat_roofs_by_elevation_map(
    #         self.basic_landuse_ascii_map_name_for_rain_garden_and_flat_roof,
    #         self.parcel_ascii_map_name_for_flat_roof,
    #         self.dem_ascii_map_name_for_flat_roof,
    #         self.minimum_flat_roof_valuable_area,
    #         self.maximum_possible_slope_for_flat_roof)
    #     flat_roof_ids_to_pixels = my_flat_roof_finder.roof_number_to_roofs
    #     cp_flat_roof_ids_to_pixels = copy.deepcopy(flat_roof_ids_to_pixels)
    #     for map_no in range(self.user_limit_on_max_maps_per_percent):
    #
    #         smallest = 100000000
    #         for i in cp_flat_roof_ids_to_pixels:
    #             if len(cp_flat_roof_ids_to_pixels[i]) < smallest:
    #                 smallest = len(cp_flat_roof_ids_to_pixels[i])
    #                 print('small:', smallest)
    #         print('final smallest:', smallest)
    #         if smallest > max_num_of_pixels:
    #             break
    #
    #         new_map_to_append = copy.deepcopy(self.basic_map_for_me)    ##########################
    #         if not cp_flat_roof_ids_to_pixels:
    #             break
    #         max_no = max_num_of_pixels
    #         new_map_pixels = {}
    #         tmp_rain_garden_ids_to_pixels = copy.deepcopy(cp_flat_roof_ids_to_pixels)
    #         flag = False
    #         for rain_id in cp_flat_roof_ids_to_pixels:
    #             num_of_rain_pixels = len(cp_flat_roof_ids_to_pixels[rain_id])
    #             if num_of_rain_pixels > max_no:
    #                 continue
    #             max_no -= num_of_rain_pixels
    #             new_map_pixels[rain_id] = cp_flat_roof_ids_to_pixels[rain_id]
    #             for pixel in new_map_pixels[rain_id]:
    #                 new_map_to_append[pixel['x']][pixel['y']] = AdvancedLandUseMap.VALUES.RAIN_GARDEN
    #             # print('map111:', new_map_pixels[rain_id])
    #             del tmp_rain_garden_ids_to_pixels[rain_id]
    #             flag = True
    #             print('deleted the bech', len(tmp_rain_garden_ids_to_pixels), len(cp_flat_roof_ids_to_pixels))
    #             # print('map222:', new_map_pixels[rain_id])
    #         cp_flat_roof_ids_to_pixels = tmp_rain_garden_ids_to_pixels
    #
    #         # print('smallest cp:', len(cp_flat_roof_ids_to_pixels))
    #         # print('new_map to append:', new_map_to_append)
    #         if flag:
    #             print('appended!')
    #             new_maps.append(new_map_to_append)
    #         print('new map appended!', len(new_maps))
    #     return new_maps
    #
    # def build_rain_garden_maps_for_priority_item_with_percentage(self, max_num_of_pixels):
    #     new_maps = []
    #     print('rain garden2')
    #     my_rain_garden_finder = RainGardenFinder()
    #     rain_garden_output = my_rain_garden_finder.get_rain_gardens(
    #         self.basic_landuse_ascii_map_name_for_rain_garden_and_flat_roof,
    #         self.minimum_rain_garden_valuable_area)
    #     rain_garden_ids_to_pixels = my_rain_garden_finder.rain_garden_ids_to_pixels
    #     cp_rain_garden_ids_to_pixels = copy.deepcopy(rain_garden_ids_to_pixels)
    #     for map_no in range(self.user_limit_on_max_maps_per_percent):
    #
    #         smallest = 100000000
    #         for i in cp_rain_garden_ids_to_pixels:
    #             if len(cp_rain_garden_ids_to_pixels[i]) < smallest:
    #                 smallest = len(cp_rain_garden_ids_to_pixels[i])
    #                 print('small:', smallest)
    #         print('final smallest:', smallest)
    #         if smallest > max_num_of_pixels:
    #             break
    #
    #         new_map_to_append = copy.deepcopy(self.basic_map_for_me)    #############################
    #         if not cp_rain_garden_ids_to_pixels:
    #             break
    #         max_no = max_num_of_pixels
    #         new_map_pixels = {}
    #         tmp_rain_garden_ids_to_pixels = copy.deepcopy(cp_rain_garden_ids_to_pixels)
    #         flag = False
    #         for rain_id in cp_rain_garden_ids_to_pixels:
    #             num_of_rain_pixels = len(cp_rain_garden_ids_to_pixels[rain_id])
    #             if num_of_rain_pixels > max_no:
    #                 continue
    #             max_no -= num_of_rain_pixels
    #             new_map_pixels[rain_id] = cp_rain_garden_ids_to_pixels[rain_id]
    #             for pixel in new_map_pixels[rain_id]:
    #                 new_map_to_append[pixel['x']][pixel['y']] = AdvancedLandUseMap.VALUES.RAIN_GARDEN
    #             # print('map111:', new_map_pixels[rain_id])
    #             del tmp_rain_garden_ids_to_pixels[rain_id]
    #             flag = True
    #             print('deleted the bech', len(tmp_rain_garden_ids_to_pixels), len(cp_rain_garden_ids_to_pixels))
    #             # print('map222:', new_map_pixels[rain_id])
    #         cp_rain_garden_ids_to_pixels = tmp_rain_garden_ids_to_pixels
    #
    #
    #         # print('smallest cp:', len(cp_rain_garden_ids_to_pixels))
    #         # print('new_map to append:', new_map_to_append)
    #         if flag:
    #             print('appended!')
    #             new_maps.append(new_map_to_append)
    #         print('new map appended!', len(new_maps))
    #     return new_maps


    # def build_continuous_maps_for_priority_item(self):
    #     step = 5
    #     maps_for_priority = {'maps': {}, 'final': None}
    #     print('start:')
    #     for i in range(1, int(100/step) + 1):
    #         print('i:', i)
    #         percent = step * i
    #         print('%:', percent)
    #         maps = [[]]
    #         # maps = self.build_maps_for_priority_item_with_percentage(percent)
    #         print('maps len:', len(maps))
    #         maps_for_priority['maps'][percent] = maps
    #         if percent == 100:
    #             maps_for_priority['final'] = maps[0]    # should not be empty!!
    #         print('maps for priority:', maps_for_priority)
    #     self.priority_maps[self.priority_item] = maps_for_priority
    #     print('final priority maps:', self.priority_maps)

    def build_continuous_maps_for_priority_item_with_percentage(self, num_of_pixels, percent):
        print('continuous2')
        maps = []
        priority_item = self.priority_item
        print('priority item:', priority_item)
        main_map = copy.deepcopy(self.advanced_landuse_map.map)
        matrix = main_map.matrix
        for map_no in range(self.user_limit_on_max_maps_per_percent):
            new_map_to_append = copy.deepcopy(self.basic_map_for_new_priority)    ###############################
            seen_pixels = 0
            for i in range(len(matrix)):
                # print('i:', i)
                # print('seen pixels:', seen_pixels)
                # print('num of pixels:', num_of_pixels)
                # print('seen pixels > num of pixels:', seen_pixels > num_of_pixels)
                if seen_pixels > num_of_pixels:
                    # print('seen pixels > num_of_pixels111:', seen_pixels)
                    break
                col = matrix[i]
                for j in range(len(col)):
                    # print('j:', j)
                    if seen_pixels > num_of_pixels:
                        # print('seen pixels > num_of_pixels222:', seen_pixels)
                        break
                    it = matrix[i][j]
                    # print('matrix[i][j]:', matrix[i][j])
                    if it == priority_item:
                        matrix[i][j] = main_map.no_data_value
                        # print('it = priority item = ', it)
                        # print('i:', i, ', j:', j)
                        seen_pixels += 1
                        # print('seen_pixels:', seen_pixels)
                        new_map_to_append.matrix[i][j] = it
                        # main_map.matrix[i][j] = self.basic_landuse_map.map.matrix[i][j]
            else:
                # print('seen pixels > num_of_pixels333:', seen_pixels)
                maps.append({'map': new_map_to_append, 'num_of_pixels:': seen_pixels})
                # print('maps len111:', len(maps))
                break
            maps.append({'map': new_map_to_append, 'num_of_pixels:': seen_pixels})
            print('maps len222:', len(maps))
        return maps


class UserMergeForAlgorithmsTest:
    # def test_get_priorities(self):
    #     basic_landuse_map = map_loader.load_map(LandUseMap, "landuse.asc")
    #     advanced_landuse_map = map_loader.load_map(DetailedLandUseMap, "landuse.asc")
    #
    #     print('taha map:', advanced_landuse_map.map.get_config_string())
    #     print('landuse map:', basic_landuse_map.map.get_config_string())
    #     a = UserMergeForAlgorithms().get_priorities(
    #         [5], basic_landuse_map, advanced_landuse_map,
    #         "landuse.asc", 10,
    #         "roof30true.asc", "elevation.asc", 10, 5,
    #         30)

    def test_get_priorities_in_clean_way(self):
        LANDUSE_NAME = 'land_use_ascii_map_name'
        MIN_AREA = 'minimum_valuable_area'
        PARCEL_NAME = 'parcel_ascii_map_name'
        DEM_NAME = 'dem_ascii_map_name'
        MAX_SLOPE = 'max_possible_slope_for_flat_roof'

        basic_landuse_map = map_loader.load_map(LandUseMap, 'landuse.asc')
        advanced_landuse_map = map_loader.load_map(DetailedLandUseMap, "landuse.asc")
        print('taha:', advanced_landuse_map.map.get_config_string())
        print('landuse:', basic_landuse_map.map.get_config_string())
        a = UserMergeForAlgorithms().get_priorities_in_clean_way(
            [5], basic_landuse_map, advanced_landuse_map, 12,
            {LANDUSE_NAME: 'landuse.asc', MIN_AREA: '10'},
            {LANDUSE_NAME: 'landuse.asc',
             PARCEL_NAME: 'roof30true.asc',
             DEM_NAME: 'elevation.asc',
             MIN_AREA: '20', MAX_SLOPE: '5'})


UserMergeForAlgorithmsTest().test_get_priorities_in_clean_way()
# ChooseStuff().choose_all_situations_of_n(322)
class ChooseStuff2:
    nth_list = {}

    def limit(self, n):
        if n < 10:
            return 600000
        if n < 15:
            return 1000000
        if n < 20:
            return 2000000
        if n < 25:
            return 3000000
        return 2500000
        # if n < 10:
        #     return 2000000
        # if n < 15:
        #     return 2000000
        # if n < 20:
        #     return max(50*n*n, 100000)
        # if n < 30:
        #     return max(50*n*n, 50000)
        return 2000000

    def build(self, n):
        t = time.time()
        self.nth_list[1] = []
        for i in range(n):
            # print(i)
            self.nth_list[1].append([i])
        for i in range(2, n + 1):
            print(i)
            self.nth_list[i] = []
            # print('i - 1 list:', self.nth_list[i-1])
            limit = self.limit(i)
            index = 0
            for j in reversed(self.nth_list[i-1]):
                # print('j:', j)
                mm = 0
                for k in reversed(range(j[0])):
                    # if i == 23:
                    #     mm+=1
                    #     if mm > 1000000:
                    #         mm = 0
                    #         print('another mil', index)
                    self.nth_list[i].append([k] + j)
                    # print('nth:', self.nth_list[i])
                    index += 1
                    if index >= limit:
                        break
                if index >= limit:
                    print(time.time() - t)
                    break
            print('len:', len(self.nth_list[i]))
        return self.nth_list


# t = time.time()
# a = ChooseStuff2().build(322)
# for i in a:
#     print('i:', i, len(a[i]))
#     if len(a[i]) == 0:
#         print(i)
#         break
#
# print(time.time() - t)