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
        'id': 16,
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
        # for index in range(len(self.subs)):
        #     self.subs[index][SubConsts.ID] = index
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
                self.max_id = 1
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
        if self.is_flat_roof_priority(self.priority):
            self.build_id_to_pixels_for_flat_roof_priority()
        else:
            self.calculate_id_to_pixels_for_priority()
        # else:
        self.add_priority_as_needed()

    def is_flat_roof_priority(self, priority):
        if priority[PriorityConsts.PIXEL_CODE] == AdvancedLandUseMap.VALUES.GREEN_ROOF:
            return True
        return False

    def add_priority_as_needed(self):
        sub_id = self.sub[SubConsts.ID]
        pixel_code = self.priority[PriorityConsts.PIXEL_CODE]
        # self.calculate_id_to_pixels_for_priority()
        id_to_pixels = self.id_t_p
        max_needed = self.num_of_needed_pixels
        self.sort_id_to_pixels(id_to_pixels)
        for id in self.ids_list:
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

    def build_id_to_pixels_for_flat_roof_priority(self):
        id_to_pixels = {}
        basic_landuse_name = self.sub[SubConsts.BASIC_LANDUSE_MAP_NAME]
        parcel_name = self.sub[SubConsts.PARCEL_MAP_NAME]
        dem_name = self.sub[SubConsts.ELEVATION_MAP_NAME]
        min_val_area_for_roof = self.sub[SubConsts.MIN_VALUABLE_AREA_FOR_FLAT_ROOF]
        max_slope = self.sub[SubConsts.MAX_POSSIBLE_SLOPE]
        pixel_code = self.priority[PriorityConsts.PIXEL_CODE]
        fd = FlatRoofFinder()
        output = fd.get_flat_roofs_by_elevation_map(basic_landuse_name,
                                                    parcel_name,
                                                    dem_name,
                                                    min_val_area_for_roof,
                                                    max_slope)
        id_to_pixels = fd.roof_number_to_roofs
        self.id_t_p = id_to_pixels

    def add_discrete_priority_as_needed(self):
        sub_id = self.sub[SubConsts.ID]
        pixel_code = self.priority[PriorityConsts.PIXEL_CODE]
        id_to_pixels = self.build_id_to_pixels_for_discrete_priority()
        max_needed = self.num_of_needed_pixels
        self.sort_id_to_pixels(id_to_pixels)
        for id in self.ids_list:
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

    def sort_id_to_pixels(self, id_to_pixels):
        self.ids_list = reversed(sorted(id_to_pixels, key=lambda id: len(id_to_pixels[id])))

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

    def build_new_id_for_pixel(self, i, j):
        self.max_id += 1
        self.id_t_p[self.max_id] = []
        self.id_t_p[self.max_id].append({'x': i, 'y': j})
        return self.max_id

    def calculate_id_to_pixels_for_priority(self):
        self.id_t_p = {}
        self.pixel_code = self.priority[PriorityConsts.PIXEL_CODE]
        self.advanced_map = self.sub[SubConsts.ADVANCED_LANDUSE_MAP]
        self.flag_map = deepcopy(self.advanced_map.map)
        for i in range(len(self.flag_map.matrix)):
            for j in range(len(self.flag_map.matrix[i])):
                self.flag_map.matrix[i][j] = False

        self.id_map = deepcopy(self.advanced_map.map)
        for i in range(len(self.id_map.matrix)):
            for j in range(len(self.id_map.matrix[i])):
                self.id_map.matrix[i][j] = 0

        for i in range(len(self.advanced_map.map.matrix)):
            row = self.advanced_map.map.matrix[i]
            for j in range(len(row)):
                cell = row[j]
                if cell != self.pixel_code:
                    continue
                if self.id_map.matrix[i][j] == 0:
                    self.id_map.matrix[i][j] = self.build_new_id_for_pixel(i, j)
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if x < 0 or y < 0 or \
                                        x >= self.advanced_map.map.n_rows or \
                                        y >= self.advanced_map.map.n_cols:
                            continue
                        if x == i and y == j:
                            continue
                        if self.advanced_map.map.matrix[x][y] != cell:
                            continue
                        if self.id_map.matrix[x][y] == self.id_map.matrix[i][j]:
                            continue
                        if not self.flag_map.matrix[x][y]:
                            self.flag_map.matrix[x][y] = True
                            self.set_new_pixel_with_new_range(x, y, i, j)
                        else:
                            self.set_all_pixels_in_new_range_with_ones_in_old_range(i, j, x, y)
        if self.priority[PriorityConsts.PIXEL_CODE] == AdvancedLandUseMap.VALUES.RAIN_GARDEN:
            min_val_area_for_rain = self.sub[SubConsts.MIN_VALUABLE_AREA_FOR_RAIN_GARDEN] / \
                                    self.sub[SubConsts.ADVANCED_LANDUSE_MAP].map.cell_size
            self.delete_ids_smaller_than(min_val_area_for_rain)
        return self.id_t_p

    def delete_ids_smaller_than(self, size):
        id_tp_cp = copy.deepcopy(self.id_t_p)
        for i in self.id_t_p:
            if len(self.id_t_p) < size:
                del id_tp_cp
        self.id_t_p = id_tp_cp

    def set_new_pixel_with_new_range(self, x, y, i, j):
        id = self.id_map.matrix[i][j]
        self.id_t_p[id].append({"x": x, "y": y})
        self.id_map.matrix[x][y] = id

    def set_all_pixels_in_new_range_with_ones_in_old_range(self, i, j, x, y):
        id_that_should_be_deleted = self.id_map.matrix[i][j]
        main_id = self.id_map.matrix[x][y]
        pixels_that_should_go_to_main_id = self.id_t_p[id_that_should_be_deleted]
        for pixel in pixels_that_should_go_to_main_id:
            self.id_map.matrix[pixel['x']][pixel['y']] = main_id
            self.id_t_p[main_id].append(pixel)
        self.id_t_p[id_that_should_be_deleted] = []

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


class RegionHandlerWithLogicalInput:
    def __init__(self):
        self.cost_optimizer = CostOptimizerForSubs()

    def build_region_source_by(self, region_sink):
        region_source = {}
        for sink in region_sink:
            print("sink:", region_sink)
            for src in region_sink[sink]:
                if src not in region_source:
                    region_source[src] = [sink]
                else:
                    src_sink = region_source[src]
                    if sink not in src_sink:
                        region_source[src].append(sink)
        return region_source

    def init(self, subs, region_sink, user_priorities):
        self.region_source = self.build_region_source_by(region_sink)
        self.region_sink = region_sink
        self.subs = subs
        self.priorities = user_priorities
        for i in self.region_sink:
            print("sink:", i, "sources:", self.region_sink[i])
        for i in self.region_source:
            print("source:", i, "sinks:", self.region_source[i])

    def handle_regions(self, subs, region_sink, user_priorities):
        self.init(subs, region_sink, user_priorities)
        self.regions_by_alg_1 = self.get_regions_by_alg_1()
        self.regions_by_alg_2 = self.get_regions_by_alg_2()
        self.regions_by_alg_3 = self.get_regions_by_alg_3()
        self.regions_by_alg_4 = self.get_regions_by_alg_4()
        alg1_maps = self.cost_optimizer.optimize_cost_for_subs(self.regions_by_alg_1, self.priorities)
        alg2_maps = self.cost_optimizer.optimize_cost_for_subs(self.regions_by_alg_2, self.priorities)
        alg3_maps = self.cost_optimizer.optimize_cost_for_subs(self.regions_by_alg_3, self.priorities)
        alg4_maps = self.cost_optimizer.optimize_cost_for_subs(self.regions_by_alg_4, self.priorities)
        output = {1: alg1_maps, 2: alg2_maps, 3: alg3_maps, 4: alg4_maps}
        return output

    def get_regions_by_alg_1(self):
        regions = []
        for sub in self.subs:
            sub_id = int(sub[SubConsts.ID])
            if sub_id in self.region_source and sub[SubConsts.EXTRA_VOLUME > 0]:
                regions.append(sub)
        #
        # for i in self.region_source:
        #     for j in self.subs:
        #         if int(j[SubConsts.ID]) == int(i):
        #             if j[SubConsts.EXTRA_VOLUME] > 0:
        #                 regions.append(j)
        return regions

    def get_regions_by_alg_2(self):
        regions = []
        src_regions = self.get_regions_by_alg_1()
        for sub in self.subs:
            sub_id = int(sub[SubConsts.ID])
            if sub_id in self.region_sink and sub[SubConsts.EXTRA_VOLUME > 0]:
                if sub not in regions:
                    regions.append(sub)
        #
        # for i in self.region_sink:
        #     for j in self.subs:
        #         if int(j[SubConsts.ID]) == int(i):
        #             if j[SubConsts.EXTRA_VOLUME] > 0:
        #                 if j not in regions:
        #                     regions.append(j)
        return regions

    def get_regions_by_alg_3(self):
        return []

    def get_regions_by_alg_4(self):
        reg3 = self.get_regions_by_alg_3()
        reg2 = self.get_regions_by_alg_2()
        reg4 = []
        reg4.extend(reg3)
        for i in reg2:
            if i not in reg3:
                reg4.append(i)
        return reg4


class FloodDataBuilder:
    def build_flooding_data_with_max_node(self, rpt_file, max_node):
        all_nodes_with_max_number = {}
        rpt_nodes = self.build_flooding_data(rpt_file)
        for i in range(max_node):
            all_nodes_with_max_number[i] = rpt_nodes.get(i, 0)
        return all_nodes_with_max_number

    def build_flooding_data(self, rpt_file):
        nodes = self.build_basic_data(rpt_file)
        ret_nodes = {}
        for node in nodes:
            ret_nodes[int(node[0])] = node[5]
        return ret_nodes

    def build_basic_data(self, rpt_file):
        rpt = open(rpt_file, "r")

        # ---- Find Node Flooding Summary -----
        check = True
        while check:
            line1 = rpt.readline()
            if "Node Flooding Summary" in line1:
                check2 = True
                while check2:

                    line1 = rpt.readline()
                    if "Node" in line1:
                        line1 = rpt.readline()
                        line1 = rpt.readline()

                        check3 = True
                        while check3:
                            if "*" in line1:
                                check3 = False

                            line1 += rpt.readline()

                        check = False
                        check2 = False

        Node_FS = []
        a = line1.split("\n")

        for i in range(len(a)):
            Node_FS.append([])
            line1 = str(a[i])
            a[i] = line1.split(" ")
            for j in a[i]:
                if j != '':
                    Node_FS[i].append(j)
        node = []
        for n in Node_FS:
            if len(n) == 7:
                node.append(n)
        return node


class RegionHandler:
    def __init__(self):
        self.logical_handler = RegionHandlerWithLogicalInput()
        self.flood_builder = FloodDataBuilder()

    def handle_regions(self, rpt_file, subs, subs_sink, priorities, max_node_number):
        subs_with_extra_volume = self.flood_builder.build_flooding_data_with_max_node(rpt_file, max_node_number)
        print("ids:", subs_with_extra_volume)
        for sub in subs:
            print("old:", sub)
            sub_id = sub[SubConsts.ID]
            extra_volume = subs_with_extra_volume.get(sub_id, 0)
            sub[SubConsts.EXTRA_VOLUME] = extra_volume
            print("sub:", sub)
        output_maps = self.logical_handler.handle_regions(subs, subs_sink, priorities)
        return output_maps

m = RegionHandler().handle_regions("report.rpt", basic_subs, {1:[1]}, basic_priorities, 32)
print("m:", m)
# RegionHandler().handle_regions({}, {1: [2.3], 2: [3]}, {1: [2, 3], 2: [3, 4], 4: [1, 2]})

# a = CostOptimizerForSubs()
# output = a.optimize_cost_for_subs(basic_subs, basic_priorities)
# print("max priorities for sub:::", a.priority_pixels_for_sub)
# print("final cost:", output["final_price"])
# print("detailed cost:", output["detailed_price"])
# maps = output["maps"]
# for i in maps:
#     map = maps[i]
#     print("file name:", i)
#     map.to_file(str(i) + ".asc")

