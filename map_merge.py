from copy import deepcopy

from maps import *
from map_loader import MapLoader
from cost_optimization import *

map_loader = MapLoader()


class MapMerge:
    def __init__(self):
        self.water_shed_map = None
        self.water_shed_matrix = None

    def get_map_name_by(self, id, basic_name):
        return "reg_" + str(float(id)) + "_" + str(basic_name)

    def build_watershed_id_to_pixels(self):
        water_shed_id_to_pixels = {}
        for i in range(len(self.water_shed_matrix)):
            row = self.water_shed_matrix[i]
            for j in range(len(row)):
                cell = row[j]
                if cell == self.water_shed_map.no_data_value:
                    continue
                cell_obj = water_shed_id_to_pixels.get(cell, [])
                cell_obj.append({"x": i, "y": j})
                water_shed_id_to_pixels[cell] = cell_obj
        return water_shed_id_to_pixels

    def merge_outputs_to_one_by_watershed_map(self, water_shed_map_name, maps, final_name):
        self.water_shed_map = map_loader.load_map(WaterShedMap, water_shed_map_name).map
        self.water_shed_matrix = self.water_shed_map.matrix
        water_shed_id_to_pixels = self.build_watershed_id_to_pixels()
        output_map = Map()
        output_map.set_config(self.water_shed_map)
        self.water_shed_map = None
        self.water_shed_matrix = None
        for i in range(output_map.n_rows):
            output_map.matrix.append([])
            for j in range(output_map.n_cols):
                output_map.matrix[i].append(output_map.no_data_value)
        print("maps:", maps)
        # if maps["maps"] == {}:
        #     print("empty map!")
        #     return
        for id in water_shed_id_to_pixels:
            print("id:", id)
            if maps["maps"].get(id) is None:
                print("continued")
                continue
            map_name = maps["maps"][id]
            map_obj = map_loader.load_map(BasicMap, map_name).map
            print("getting into pixels:::")
            for pixel in water_shed_id_to_pixels[id]:
                # print("pixel::::", pixel)
                output_map.matrix[pixel["x"]][pixel["y"]] = map_obj.matrix[pixel["x"]][pixel["y"]]
        print("final name:", final_name)
        output_map.to_file(final_name)

    def build_maps_by_watershed_map(self, water_shed_map_name, other_maps_names):
        # other maps names format: {"basic_land_use_map":"landuse.asc, "advanced_land_use_map":"final.asc",}
        self.water_shed_map = map_loader.load_map(WaterShedMap, water_shed_map_name).map
        self.water_shed_matrix = self.water_shed_map.matrix
        water_shed_i_len = self.water_shed_map.n_rows
        water_shed_j_len = self.water_shed_map.n_cols
        water_shed_id_to_pixels = self.build_watershed_id_to_pixels()
        self.water_shed_map = None
        self.water_shed_matrix = None
        for id in water_shed_id_to_pixels:
            print("id", id)

        output = {}
        for id in water_shed_id_to_pixels:
            output[id] = {}
        for map_name in other_maps_names:
            other_map = map_loader.load_map(BasicMap, other_maps_names[map_name]).map
            output_map = {}
            for id in water_shed_id_to_pixels:
                output_map[id] = Map()
                output_map[id].set_config(other_map)

                for i in range(water_shed_i_len):
                    output_map[id].matrix.append([])
                    for j in range(water_shed_j_len):
                        output_map[id].matrix[i].append(output_map[id].no_data_value)

                pixels_for_id = water_shed_id_to_pixels[id]
                for pixel in pixels_for_id:
                    output_map[id].matrix[pixel["x"]][pixel["y"]] = \
                        other_map.matrix[pixel["x"]][pixel["y"]]
                new_name = self.get_map_name_by(id, other_maps_names[map_name])
                print("before::")
                output_map[id].to_file(new_name)
                output_map[id] = None
                output[id][map_name] = new_name
                print("id:", id)
        print("done!")

        # for id in output_maps:
        #     output[id] = {}
        #     for map_name in output_maps[id]:
        #         new_name = self.get_map_name_by(id, map_name)
        #         print("before")
        #         output_maps[id][map_name].to_file(new_name)
        #         print("after")
        #         output[id][map_name] = new_name
        #         print("map:", map_name, "done!")
        #     print("id:", id, "done")
        return output


class RptInpDataBuilder:
    def build_graph(self, inp_file):
        graph = {}
        nodes = self.build_basic_data_for_graph(inp_file)
        for node in nodes:
            from_node = int(node[1])
            to_node = int(node[2])
            if graph.get(to_node) is not None:
                print("graph for to exist:", to_node)
            graph[to_node] = graph.get(to_node, [])
            graph[to_node].append(from_node)
        for i in graph:
            print("to:", i)
            print("from:", graph[i])
        return graph

    def build_basic_data_for_graph(self, inp_file):
        rpt = open(inp_file, "r")
        while True:
            line = rpt.readline()
            if "[CONDUITS]" in line:
                rpt.readline()
                rpt.readline()
                data_line = ""
                should_break = False
                while True:
                    line = rpt.readline()
                    if "[PUMPS]" in line:
                        should_break = True
                        break
                    data_line += line
                if should_break:
                    break
        a = data_line.split("\n")
        basic_node = []
        for i in range(len(a)):
            basic_node.append([])
            line1 = str(a[i])
            a[i] = line1.split(" ")
            for j in a[i]:
                if j != '':
                    basic_node[i].append(j)
        node = []
        for n in basic_node:
            if len(n) == 9:
                node.append(n)
        return node

    def build_inflow_data_with_max_node(self, rpt_file, max_node):
        all_nodes_with_max_number = {}
        rpt_nodes = self.build_inflow_data(rpt_file)
        for i in range(1, max_node + 1):
            all_nodes_with_max_number[i] = rpt_nodes[i]
        return all_nodes_with_max_number

    def build_inflow_data(self, rpt_file):
        nodes = self.build_basic_data_for_inflow(rpt_file)
        ret_nodes = {}
        for node in nodes:
            print("node:", node)
            ret_nodes[int(node[0])] = {SubConsts.LATERAL_INFLOW: float(node[6]) * 1000000,
                                       SubConsts.TOTAL_INFLOW: float(node[7]) * 1000000}
        return ret_nodes

    def build_basic_data_for_inflow(self, rpt_file):
        rpt = open(rpt_file, "r")

        # ---- Find Node Flooding Summary -----
        check = True
        while check:
            line1 = rpt.readline()
            if "Node Inflow Summary" in line1:
                check2 = True
                while check2:

                    line1 = rpt.readline()
                    if "Node" in line1:
                        line1 = rpt.readline()
                        line1 = rpt.readline()

                        check3 = True
                        while check3:
                            new_line = rpt.readline()
                            if "WMB_STORAGE" in new_line:
                                break

                            line1 += new_line

                        check = False
                        check2 = False

        Node_IS = []
        a = line1.split("\n")

        for i in range(len(a)):
            Node_IS.append([])
            line1 = str(a[i])
            a[i] = line1.split(" ")
            for j in a[i]:
                if j != '':
                    Node_IS[i].append(j)
        node = []
        for n in Node_IS:
            if len(n) >= 9:
                node.append(n)
        return node

    def build_flooding_data_with_max_node(self, rpt_file, max_node):
        all_nodes_with_max_number = {}
        rpt_nodes = self.build_flooding_data(rpt_file)
        for i in range(1, max_node + 1):
            all_nodes_with_max_number[i] = rpt_nodes.get(i, 0)
        extra_nodes = {}
        for rpt_node_id in rpt_nodes:
            if rpt_node_id > max_node:
                extra_nodes[rpt_node_id] = rpt_nodes[rpt_node_id]
        all_nodes_with_max_number[SubConsts.EXTRA_SUB] = extra_nodes
        return all_nodes_with_max_number

    def build_flooding_data(self, rpt_file):
        nodes = self.build_basic_data_for_flood(rpt_file)
        ret_nodes = {}
        for node in nodes:
            ret_nodes[int(node[0])] = float(node[5]) * 1000000
        return ret_nodes

    def build_basic_data_for_flood(self, rpt_file):
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


# class RegionHandler:
#     def __init__(self):
#         self.logical_handler = RegionHandlerWithLogicalInput()
#         self.flood_builder = RptInpDataBuilder()
#
#     def handle_regions(self, rpt_file, subs, subs_sink, priorities, max_node_number):
#         subs_with_extra_volume = self.flood_builder.build_flooding_data_with_max_node(rpt_file, max_node_number)
#         for sub in subs:
#             sub_id = sub[SubConsts.ID]
#             extra_volume = subs_with_extra_volume.get(sub_id, 0)
#             sub[SubConsts.EXTRA_VOLUME] = extra_volume
#         output_maps = self.logical_handler.handle_regions(subs, subs_sink, priorities)
#         return output_maps


class RegionBuilder:
    def __init__(self):
        self.map_marge = MapMerge()
        self.flood_data_builder = RptInpDataBuilder()
        self.overlay = Overlay()

    def merge_maps_by_water_shed_map(self, watershed_map_name, output_maps, landuse_map_name):
        for alg in output_maps:
            maps_for_output = output_maps[alg]
            alg_name = "alg_" + str(alg) + "_"
            final_name_only = alg_name + "only_" + maps_for_output["final_name"]
            self.map_marge.merge_outputs_to_one_by_watershed_map(watershed_map_name, maps_for_output, final_name_only)
            final_map = self.overlay.overlay_with_landuse(final_name_only, landuse_map_name)
            final_name = alg_name + maps_for_output["final_name"]
            final_map.to_file(final_name)

    ###
    def build_subs_for_regions(self, water_shed_map_name,
                               basic_land_use_map_name,
                               advanced_land_use_map_name,
                               parcel_map_name,
                               dem_map_name,
                               rpt_file, max_node_number, what_percent_to_be_source,
                               min_rain, min_flat, max_slope,
                               use_existing_region_maps):

        input_maps = {SubConsts.BASIC_LANDUSE_MAP: basic_land_use_map_name,
                      SubConsts.ADVANCED_LANDUSE_MAP: advanced_land_use_map_name,
                      SubConsts.PARCEL_MAP: parcel_map_name,
                      SubConsts.ELEVATION_MAP: dem_map_name}
        ####################
        if not use_existing_region_maps:
            region_maps = self.map_marge.build_maps_by_watershed_map(water_shed_map_name, input_maps)
        ####################
        subs_with_extra_volume = self.flood_data_builder.build_flooding_data_with_max_node(rpt_file, max_node_number)
        subs_with_inflow = self.flood_data_builder.build_inflow_data_with_max_node(rpt_file, max_node_number)
        for i in subs_with_inflow:
            print("id:", i)
            print("data:", subs_with_inflow[i])
        region_maps = {
            i: {input_map: self.map_marge.get_map_name_by(i, input_maps[input_map]) for input_map in input_maps} for i
            in
            subs_with_inflow}
        print("regions::")
        for i in region_maps:
            print("id:", i)
            print("regions:", region_maps[i])
        # for i in region_maps:
        #     region_maps[i] = {SubConsts.BASIC_LANDUSE_MAP: "landuse.asc",
        #                       SubConsts.ADVANCED_LANDUSE_MAP: "Final.asc",
        #                       SubConsts.PARCEL_MAP: "parcel.asc",
        #                       SubConsts.ELEVATION_MAP: "dem.asc"}
        subs = []
        for id in region_maps:
            region_extra_volume = subs_with_extra_volume[id]
            region_inflow = subs_with_inflow[id]
            print("sub:::::::::::", id, "inflow:", region_inflow)
            sub = {SubConsts.ID: id, SubConsts.BASIC_LANDUSE_MAP: region_maps[id][SubConsts.BASIC_LANDUSE_MAP],
                   SubConsts.ADVANCED_LANDUSE_MAP: region_maps[id][SubConsts.ADVANCED_LANDUSE_MAP],
                   SubConsts.PARCEL_MAP: region_maps[id][SubConsts.PARCEL_MAP],
                   SubConsts.ELEVATION_MAP: region_maps[id][SubConsts.ELEVATION_MAP],
                   SubConsts.EXTRA_VOLUME: region_extra_volume, SubConsts.INFLOW: region_inflow,
                   SubConsts.MIN_VALUABLE_AREA_FOR_RAIN_GARDEN: min_rain,
                   SubConsts.MIN_VALUABLE_AREA_FOR_FLAT_ROOF: min_flat, SubConsts.MAX_POSSIBLE_SLOPE: max_slope,
                   SubConsts.IS_SOURCE: self.is_source(region_inflow, what_percent_to_be_source),
                   SubConsts.IS_REAL_SUB: True}
            subs.append(sub)
            print("sub:", id, "is source:", sub[SubConsts.IS_SOURCE])
        extra_subs = []
        for extra_sub in subs_with_extra_volume[SubConsts.EXTRA_SUB]:
            sub = {SubConsts.ID: extra_sub,
                   SubConsts.EXTRA_VOLUME: subs_with_extra_volume[SubConsts.EXTRA_SUB][extra_sub],
                   SubConsts.IS_REAL_SUB: False,
                   SubConsts.IS_SOURCE: False}
            extra_subs.append(sub)
        return subs, extra_subs

    def is_source(self, reg_inflow, source_percent):
        lateral_inflow = reg_inflow[SubConsts.LATERAL_INFLOW]

        total_inflow = reg_inflow[SubConsts.TOTAL_INFLOW]
        is_source = float(lateral_inflow) / float(total_inflow) >= source_percent
        return is_source


# a = RegionBuilder().build_subs_for_regions("watershed_cost.asc", "landuse.asc", "Final.asc", "parcel.asc", "elevation.asc", "report.rpt", 32, 15, 10, 0.5)
# for i in a:
#     print(i)


class Main:
    def __init__(self):
        self.region_builder = RegionBuilder()
        self.logical_handler = RegionHandlerWithLogicalInput()

        self.water_shed_map_name = None
        self.basic_land_use_map_name = None
        self.advanced_land_use_map_name = None
        self.parcel_map_name = None
        self.dem_map_name = None
        self.rpt_file = None
        self.max_node_number = 0
        self.what_percent_to_be_source = 0
        self.min_rain = 0
        self.min_flat = 0
        self.max_slope = 0
        self.graph = None
        self.inp_file = None
        self.priorities = None
        self.subs = None
        self.extra_subs = None

    def init(self, water_shed_map_name,
             basic_land_use_map_name,
             advanced_land_use_map_name,
             parcel_map_name,
             dem_map_name,
             rpt_file, max_node_number, what_percent_to_be_source,
             min_rain, min_flat, max_slope,
             inp_file,
             priorities,
             use_existing_region_maps,
             algorithms_to_use):
        self.water_shed_map_name = water_shed_map_name
        self.basic_land_use_map_name = basic_land_use_map_name
        self.advanced_land_use_map_name = advanced_land_use_map_name
        self.parcel_map_name = parcel_map_name
        self.dem_map_name = dem_map_name
        self.rpt_file = rpt_file
        self.max_node_number = max_node_number
        self.what_percent_to_be_source = what_percent_to_be_source
        self.min_rain = min_rain
        self.min_flat = min_flat
        self.max_slope = max_slope
        self.inp_file = inp_file
        self.priorities = priorities
        self.algorithms_to_use = algorithms_to_use

        self.graph = self.region_builder.flood_data_builder.build_graph(inp_file)
        print("\nmain graph:")
        for i in self.graph:
            print(i, ":", self.graph[i])
        print("\n")
        self.subs, self.extra_subs = self.region_builder.build_subs_for_regions(water_shed_map_name,
                                                                                basic_land_use_map_name,
                                                                                advanced_land_use_map_name,
                                                                                parcel_map_name,
                                                                                dem_map_name,
                                                                                rpt_file, max_node_number,
                                                                                what_percent_to_be_source,
                                                                                min_rain, min_flat, max_slope,
                                                                                use_existing_region_maps)
        print("\nsrcs:")
        for sub in self.subs:
            if sub[SubConsts.IS_SOURCE]:
                print(sub[SubConsts.ID], "is source")

    def run(self):
        print("just run")

        output_maps = self.logical_handler.handle_regions(self.subs,
                                                          self.extra_subs,
                                                          self.graph,
                                                          self.priorities,
                                                          self.algorithms_to_use)
        print("done:::::::::")
        print("done:::::::::")
        print("done:::::::::")
        print("outputmaps:", output_maps)
        self.region_builder.merge_maps_by_water_shed_map(self.water_shed_map_name, output_maps,
                                                         self.basic_land_use_map_name)

    def run_with_init(self, water_shed_map_name,
                      basic_land_use_map_name,
                      advanced_land_use_map_name,
                      parcel_map_name,
                      dem_map_name,
                      rpt_file, max_node_number, what_percent_to_be_source,
                      min_rain, min_flat, max_slope,
                      inp_file,
                      priorities,
                      use_existing_region_maps,
                      algorithms_to_use):
        print("run with init")
        self.init(water_shed_map_name,
                  basic_land_use_map_name,
                  advanced_land_use_map_name,
                  parcel_map_name,
                  dem_map_name,
                  rpt_file, max_node_number, what_percent_to_be_source,
                  min_rain, min_flat, max_slope,
                  inp_file,
                  priorities,
                  use_existing_region_maps,
                  algorithms_to_use)
        output_maps = self.logical_handler.handle_regions(self.subs,
                                                          self.extra_subs,
                                                          self.graph,
                                                          priorities,
                                                          self.algorithms_to_use)
        print("done:::::::::")
        print("done:::::::::")
        print("done:::::::::")
        print("outputmaps:", output_maps)
        self.region_builder.merge_maps_by_water_shed_map(self.water_shed_map_name, output_maps,
                                                         basic_land_use_map_name)


print("start:")
main = Main()
main.init("watershed_cost.asc",
          "landuse.asc",
          "Final.asc",
          "parcel.asc",
          "elevation.asc",
          "report.rpt", 31, .6,
          15, 10, 0.5,
          "tmp.inp",
          basic_priorities,
          False, [1, 2, 3])
main.run()
# a = RptInpDataBuilder().build_graph("tmp.inp")
# print("aaaa:", a)