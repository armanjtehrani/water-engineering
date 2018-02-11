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
from copy import deepcopy
from algorithms import *


basic_priorities = [
    {
        'pixel_code': AdvancedLandUseMap.VALUES.RAIN_GARDEN,    # 30
        'price_per_sq_meter': .12,
        'volume_reduction_per_sq_meter': 1.135
    },
    {
        'pixel_code': AdvancedLandUseMap.VALUES.GREEN_ROOF,     # 40
        'price_per_sq_meter': .2,
        'volume_reduction_per_sq_meter': 8
    },
    {
        'pixel_code': AdvancedLandUseMap.VALUES.ROAD,
        'price_per_sq_meter': 1.2,
        'volume_reduction_per_sq_meter': 6
    },
    {
        'pixel_code': AdvancedLandUseMap.VALUES.RIPARIAN_ZONE,
        'price_per_sq_meter': .1,
        'volume_reduction_per_sq_meter': 6
    },
]


basic_subs = [
    {
        'id': 1,
        'basic_land_use_map': map_loader.load_map(LandUseMap, "landuse.asc"),
        'advanced_land_use_map': map_loader.load_map(AdvancedLandUseMap, "arman.asc"),
        'parcel_map': map_loader.load_map(ParcelMap, "roofs.asc"),  # could be not
        'dem_map': map_loader.load_map(ElevationMap, "elevation.asc"),  # could be not
        'extra_volume': 350000,
        'minimum_valuable_area_for_rain_garden': 12,
        'minimum_valuable_area_for_flat_roof': 12,
        'maximum_possible_slope': 4,
        'basic_land_use_map_name': 'landuse.asc',
        'elevation_map_name': 'elevation.asc',
        'parcel_map_name': 'roofs.asc',
    },
    # {
    #     'id': 2,
    #     'basic_land_use_map': LandUseMap(),
    #     'advanced_land_use_map': AdvancedLandUseMap(),
    #     'parcel_map': ParcelMap(),  # could be not
    #     'dem_map': ElevationMap(),  # could be not
    #     'extra_volume': 12,
    # },
    # {
    #     'id': 3,
    #     'basic_land_use_map': LandUseMap(),
    #     'advanced_land_use_map': AdvancedLandUseMap(),
    #     'parcel_map': ParcelMap(),  # could be not
    #     'dem_map': ElevationMap(),  # could be not
    #     'extra_volume': 12,
    # },
    # {
    #     'id': 4,
    #     'basic_land_use_map': LandUseMap(),
    #     'advanced_land_use_map': AdvancedLandUseMap(),
    #     'parcel_map': ParcelMap(),  # could be not
    #     'dem_map': ElevationMap(),  # could be not
    #     'extra_volume': 12,
    # },
]


class PriorityConsts:
    PIXEL_CODE = 'pixel_code'
    PRICE_PER_SQ_METER = 'price_per_sq_meter'
    VOLUME_REDUCTION_PER_SQ_METER = 'volume_reduction_per_sq_meter'


class SubConsts:
    ID = 'id'
    BASIC_LANDUSE_MAP = 'basic_land_use_map'
    ADVANCED_LANDUSE_MAP = 'advanced_land_use_map'
    PARCEL_MAP_NAME = 'parcel_map_name'
    ELEVATION_MAP_NAME = 'elevation_map_name'
    DEM_MAP = 'dem_map'
    EXTRA_VOLUME = 'extra_volume'
    MIN_VALUABLE_AREA_FOR_RAIN_GARDEN = "minimum_valuable_area_for_rain_garden"
    MIN_VALUABLE_AREA_FOR_FLAT_ROOF = "minimum_valuable_area_for_flat_roof"
    MAX_POSSIBLE_SLOPE = "maximum_possible_slope"
    BASIC_LANDUSE_MAP_NAME = "basic_land_use_map_name"


class CostOptimizerForSubs:
    def __init__(self):
        self.final_price = 0
        self.price_for_sub = {}
        self.priority_pixels_for_sub = {}
        self.subs = {}
        self.sub_index = 0
        self.sub = {}
        self.priorities = {}
        self.priority_index = 0
        self.priority = {}
        self.config_map = Map()
        self.output_maps = {}

    def is_continues_priority(self, priority):
        if priority[PriorityConsts.PIXEL_CODE] == AdvancedLandUseMap.VALUES.GREEN_ROOF:
            return False
        if priority[PriorityConsts.PIXEL_CODE] == AdvancedLandUseMap.VALUES.RAIN_GARDEN:
            return False
        return True

    def is_discrete_priority(self, priority):
        return not self.is_continues_priority(priority)

    def init(self, subs, priorities):
        self.final_price = 0
        self.price_for_sub = {}
        self.priority_pixels_for_sub = {}
        self.subs = subs
        self.priorities = priorities
        self.config_map = Map()
        self.output_maps = {}
        if len(self.subs) > 0:
            self.config_map = self.subs[0][SubConsts.BASIC_LANDUSE_MAP].map
        for index in range(len(self.subs)):
            self.subs[index][SubConsts.ID] = index
        self.build_basic_map_for_output_maps()

    def build_basic_map_for_output_maps(self):
        for sub in self.subs:
            sub_id = sub[SubConsts.ID]
            basic_map = sub[SubConsts.BASIC_LANDUSE_MAP].map
            self.output_maps[sub_id] = deepcopy(basic_map)

    def optimize_cost_for_subs(self, subs, priorities):
        self.init(subs, priorities)
        for sub_index in range(len(self.subs)):
            self.sub_index = sub_index
            self.sub = self.subs[sub_index]
            sub_id = self.sub[SubConsts.ID]
            self.price_for_sub[sub_id] = {}
            self.price_for_sub[sub_id]["final"] = 0
            self.extra_volume_left = self.sub[SubConsts.EXTRA_VOLUME]

            self.calculate_max_number_of_priorities_pixels_for_sub()
            for priority_index in range(len(priorities)):
                self.price = 0
                self.priority_index = priority_index
                self.priority = priorities[priority_index]
                priority_number = self.priority[PriorityConsts.PIXEL_CODE]

                self.price_for_sub[sub_id][priority_number] = 0
                print("priority:", self.priority[PriorityConsts.PIXEL_CODE])
                print("max number of priority pixels:", self.priority_pixels_for_sub[self.priority[PriorityConsts.PIXEL_CODE]])
                num_of_needed_pixels = self.calculate_num_of_needed_pixels_for_priority()
                self.num_of_needed_pixels = num_of_needed_pixels
                self.update_sub_output_map()

                self.price_for_sub[sub_id][self.priority[PriorityConsts.PIXEL_CODE]] = self.price
                self.price_for_sub[sub_id]["final"] += self.price

            self.final_price += self.price_for_sub[sub_id]["final"]

        output = {"maps": self.output_maps,
                  "final_price": self.final_price,
                  "detailed_price": self.price_for_sub}
        return output

    def calculate_max_number_of_priorities_pixels_for_sub(self):
        priority_numbers = []
        self.priority_pixels_for_sub = {}
        for pr in self.priorities:
            pn = pr[PriorityConsts.PIXEL_CODE]
            priority_numbers.append(pn)
            self.priority_pixels_for_sub[pn] = 0
        matrix = self.sub[SubConsts.ADVANCED_LANDUSE_MAP].map.matrix
        for i in range(len(matrix)):
            row = matrix[i]
            for j in range(len(row)):
                cell = row[j]
                if cell in priority_numbers:
                    self.priority_pixels_for_sub[cell] += 1
        # for i in self.priority_pixels_for_sub:
        #     print(i, ":", self.priority_pixels_for_sub[i])

    def calculate_num_of_needed_pixels_for_priority(self):   # tested
        priority_volume_per_meter = self.priority[PriorityConsts.VOLUME_REDUCTION_PER_SQ_METER]
        self.pixel_size = self.sub[SubConsts.BASIC_LANDUSE_MAP].map.cell_size
        priority_volume_per_pixel = priority_volume_per_meter * self.pixel_size
        extra_volume = self.extra_volume_left
        number_of_needed_pixels_of_priority = float(extra_volume) / priority_volume_per_pixel
        if int(number_of_needed_pixels_of_priority) != number_of_needed_pixels_of_priority:
            number_of_needed_pixels_of_priority = int(number_of_needed_pixels_of_priority+1)
        print("num of needed pixels for priority:", number_of_needed_pixels_of_priority)
        return number_of_needed_pixels_of_priority

    def update_sub_output_map(self):
        max_num_of_priority = self.priority_pixels_for_sub[self.priority[PriorityConsts.PIXEL_CODE]]
        needed_pixels = self.num_of_needed_pixels
        if needed_pixels > max_num_of_priority:
            self.add_all_priority_pixels()
            self.extra_volume_left -= (max_num_of_priority / self.pixel_size) * self.priority[PriorityConsts.VOLUME_REDUCTION_PER_SQ_METER]
            self.price = (max_num_of_priority / self.pixel_size) * self.priority[PriorityConsts.PRICE_PER_SQ_METER]
            return

        self.price = (needed_pixels / self.pixel_size) * self.priority[PriorityConsts.PRICE_PER_SQ_METER]
        self.extra_volume_left = 0
        if self.is_continues_priority(self.priority):
            self.add_continues_priority_as_needed()

        else:
            self.add_discrete_priority_as_needed()

    def add_continues_priority_as_needed(self):
        if 0 >= self.num_of_needed_pixels:
            return
        advanced_map = self.sub[SubConsts.ADVANCED_LANDUSE_MAP].map
        pixel_code = self.priority[PriorityConsts.PIXEL_CODE]
        sub_id = self.sub[SubConsts.ID]
        added = 0
        for i in range(len(advanced_map.matrix)):
            row = advanced_map.matrix[i]
            for j in range(len(row)):
                cell = row[j]
                if cell == pixel_code:
                    self.output_maps[sub_id].matrix[i][j] = pixel_code
                    added += 1
                    if added >= self.num_of_needed_pixels:
                        return

    def add_discrete_priority_as_needed(self):
        sub_id = self.sub[SubConsts.ID]
        pixel_code = self.priority[PriorityConsts.PIXEL_CODE]
        id_to_pixels = self.build_id_to_pixels_for_discrete_priority()
        max_needed = self.num_of_needed_pixels
        for id in id_to_pixels:
            if max_needed <= 0:
                return
            if len(id_to_pixels[id]) <= max_needed:
                max_needed -= len(id_to_pixels[id])
                for pixel in id_to_pixels[id]:
                    # print("pixel:", pixel)
                    self.output_maps[sub_id].matrix[pixel['x']][pixel['y']] = pixel_code
            else:
                for pixel in id_to_pixels[id]:
                    # print("pixel:", pixel)
                    # print("output:", self.output_maps[sub_id])
                    self.output_maps[sub_id].matrix[pixel['x']][pixel['y']] = pixel_code
                    max_needed -= 1
                    if max_needed <= 0:
                        return

    def build_id_to_pixels_for_discrete_priority(self):
        id_to_pixels = {}
        basic_landuse_name = self.sub[SubConsts.BASIC_LANDUSE_MAP_NAME]
        parcel_name = self.sub[SubConsts.PARCEL_MAP_NAME]
        dem_name = self.sub[SubConsts.ELEVATION_MAP_NAME]
        min_val_area_for_rain = self.sub[SubConsts.MIN_VALUABLE_AREA_FOR_RAIN_GARDEN]
        min_val_area_for_roof = self.sub[SubConsts.MIN_VALUABLE_AREA_FOR_FLAT_ROOF]
        max_slope = self.sub[SubConsts.MAX_POSSIBLE_SLOPE]
        pixel_code = self.priority[PriorityConsts.PIXEL_CODE]
        if pixel_code == AdvancedLandUseMap.VALUES.RAIN_GARDEN:
            rd = RainGardenFinder()
            output = rd.get_rain_gardens(basic_landuse_name, min_val_area_for_rain)
            id_to_pixels = rd.rain_garden_ids_to_pixels
        elif pixel_code == AdvancedLandUseMap.VALUES.GREEN_ROOF:
            fd = FlatRoofFinder()
            output = fd.get_flat_roofs_by_elevation_map(basic_landuse_name,
                                                        parcel_name,
                                                        dem_name,
                                                        min_val_area_for_roof,
                                                        max_slope)
            id_to_pixels = fd.roof_number_to_roofs
        return id_to_pixels


    def add_all_priority_pixels(self):
        advanced_map = self.sub[SubConsts.ADVANCED_LANDUSE_MAP].map
        pixel_code = self.priority[PriorityConsts.PIXEL_CODE]
        print("adding all priority pixels for priority:", pixel_code)
        sub_id = self.sub[SubConsts.ID]
        for i in range(len(advanced_map.matrix)):
            row = advanced_map.matrix[i]
            for j in range(len(row)):
                cell = row[j]
                if cell == pixel_code:
                    self.output_maps[sub_id].matrix[i][j] = pixel_code


a = CostOptimizerForSubs()
output = a.optimize_cost_for_subs(basic_subs, basic_priorities)
print("max priorities for sub:::", a.priority_pixels_for_sub)
print("final cost:", output["final_price"])
print("detailed cost:", output["detailed_price"])
maps = output["maps"]
for i in maps:
    map = maps[i]
    print("file name:", i)
    map.to_file(str(i) + ".asc")
