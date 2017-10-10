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
                        # print('fuck fuck fuck')
                    continue
                # pixel[i][j] is a roof
                # print('roof:)')
                # print('i:', i, 'j:', j)
                if self.flat_roofs.matrix[i][j] == self.flat_roofs.no_data_value:
                    # print('i am virgin:D')
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
                            # print('all the same bitch:D')
                            continue
                        if self.flat_roofs.matrix[x][y] == self.flat_roofs.no_data_value:
                            # print('new near virgin roof:D')
                            self.set_new_pixel_with_new_range(x, y, i, j)
                        else:
                            # print('bitch roof:D')
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
        # print('old virgin:', self.flat_roofs.matrix[x][y])
        self.flat_roofs.matrix[x][y] = self.flat_roofs.matrix[i][j]
        # print('new bitch:D:', self.flat_roofs.matrix[x][y])
        # print('old roof:', self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]])
        self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]].append({'x': x, 'y': y})
        # print('new roof:', self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]])

    def set_all_pixels_in_new_range_with_ones_in_old_range(self, i, j, x, y):
        roof_number_that_should_be_deleted = self.flat_roofs.matrix[i][j]
        # print('deleted roof number:', roof_number_that_should_be_deleted)
        main_roof_number = self.flat_roofs.matrix[x][y]
        # print('main roof number:', main_roof_number)
        roofs_that_should_go_to_main_roof_number = self.roof_number_to_roofs[roof_number_that_should_be_deleted]
        # print('fucked up roofs:', roofs_that_shoud_go_to_main_roof_number)
        # print('main roofs before:', self.roof_number_to_roofs[main_roof_number])
        for roof in roofs_that_should_go_to_main_roof_number:
            self.flat_roofs.matrix[roof['x']][roof['y']] = main_roof_number
            self.roof_number_to_roofs[main_roof_number].append(roof)
        # print('main roofs after:', self.roof_number_to_roofs[main_roof_number])
        self.roof_number_to_roofs[roof_number_that_should_be_deleted] = []
        # print('fucked up number:', self.roof_number_to_roofs[roof_number_that_should_be_deleted])

    def calculate_valuable_flat_roofs_by_area(self):
        minimum_pixels_to_be_useful = self.minimum_valuable_area / self.output.cell_size
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
        for key in self.roof_number_to_roofs:
            # print('flat roof number', key, ':')
            # print(self.roof_number_to_roofs[key])
            # print('len is:', len(self.roof_number_to_roofs[key]))
            if len(self.roof_number_to_roofs[key]) < minimum_pixels_to_be_useful:
                continue
            # flat roof size is good
            # print(key, 'added:)')
            for roof in self.roof_number_to_roofs[key]:
                # print('before output number i:', roof['x'], 'j:', roof['y'], 'was: ', self.output.matrix[roof['x']][roof['y']])
                self.output.matrix[roof['x']][roof['y']] = key
                # print('now output number i:', roof['x'], 'j:', roof['y'], 'is: ', self.output.matrix[roof['x']][roof['y']])
            # os.system('pause')


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
                if detailed_landuse_map.matrix[i][j] == DetailedLandUseMap.VALUES.Asphalt:
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
                    self.rain_gardens[i][j] = 0
                    # if landuse.matrix[i][j] == LandUseMap.VALUES.URBON_AND_BUILT_UP or \
                    #         parcel.matrix[i][j] != parcel.no_data_value:
                        # print('fuck fuck fuck')
                    continue
                # pixel[i][j] is a roof
                # print('roof:)')
                # print('i:', i, 'j:', j)
                if self.rain_gardens.matrix[i][j] == self.rain_gardens.no_data_value:
                    # print('i am virgin:D')
                    self.set_new_number_for_garden(i, j)
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
                            # print('all the same bitch:D')
                            continue
                        if self.rain_gardens.matrix[x][y] == self.rain_gardens.no_data_value:
                            # print('new near virgin roof:D')
                            self.set_new_pixel_with_new_range(x, y, i, j)
                        else:
                            # print('bitch roof:D')
                            self.set_all_pixels_in_new_range_with_ones_in_old_range(i, j, x, y)
                # os.system('pause')

    def set_new_number_for_garden(self, i, j):
        self.max_rain_garden_id += 1
        self.rain_garden_ids_to_pixels[self.max_rain_garden_id] = []
        self.rain_garden_ids_to_pixels[self.max_rain_garden_id].append({'x': i, 'y': j})
        self.rain_gardens.matrix[i][j] = self.max_rain_garden_id

    def set_new_pixel_with_new_range(self, x, y, i, j):
        # print('old virgin:', self.flat_roofs.matrix[x][y])
        self.rain_gardens.matrix[x][y] = self.rain_gardens.matrix[i][j]
        # print('new bitch:D:', self.flat_roofs.matrix[x][y])
        # print('old roof:', self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]])
        self.rain_garden_ids_to_pixels[self.rain_gardens.matrix[x][y]].append({'x': x, 'y': y})
        # print('new roof:', self.roof_number_to_roofs[self.flat_roofs.matrix[x][y]])

    def set_all_pixels_in_new_range_with_ones_in_old_range(self, i, j, x, y):
        rain_garden_number_that_should_be_deleted = self.rain_gardens.matrix[i][j]
        # print('deleted roof number:', roof_number_that_should_be_deleted)
        main_rain_garden_number = self.rain_gardens.matrix[x][y]
        # print('main roof number:', main_roof_number)
        rain_gardens_that_should_go_to_main_roof_number = \
            self.rain_garden_ids_to_pixels[rain_garden_number_that_should_be_deleted]
        # print('fucked up roofs:', roofs_that_shoud_go_to_main_roof_number)
        # print('main roofs before:', self.roof_number_to_roofs[main_roof_number])
        for rain_garden in rain_gardens_that_should_go_to_main_roof_number:
            self.rain_gardens.matrix[rain_garden['x']][rain_garden['y']] = main_rain_garden_number
            self.rain_garden_ids_to_pixels[main_rain_garden_number].append(rain_garden)
        # print('main roofs after:', self.roof_number_to_roofs[main_roof_number])
        self.rain_garden_ids_to_pixels[rain_garden_number_that_should_be_deleted] = []
        # print('fucked up number:', self.roof_number_to_roofs[roof_number_that_should_be_deleted])

    def calculate_valuable_rain_gardens_by_area(self):
        minimum_pixels_to_be_useful = self.minimum_valuable_area / self.output.cell_size
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
        for key in self.rain_garden_ids_to_pixels:
            # print('flat roof number', key, ':')
            # print(self.roof_number_to_roofs[key])
            # print('len is:', len(self.roof_number_to_roofs[key]))
            if len(self.rain_garden_ids_to_pixels[key]) < minimum_pixels_to_be_useful:
                continue
            # flat roof size is good
            # print(key, 'added:)')
            for rain_garden in self.rain_garden_ids_to_pixels[key]:
                # print('before output number i:', roof['x'], 'j:', roof['y'], 'was: ', self.output.matrix[roof['x']][roof['y']])
                self.output.matrix[rain_garden['x']][rain_garden['y']] = key
                # print('now output number i:', roof['x'], 'j:', roof['y'], 'is: ', self.output.matrix[roof['x']][roof['y']])
            # os.system('pause')








