from algorithms import *
from maps import Map
from maps import WaterShellMap
#import os

class HighPotentialArea:
    def __init__(self, hydrology=False, hydrolic=False, **runoff_landa):

        if hydrology:
            hydrology(self, **runoff_landa)
        if hydrolic:
            pass
        if hydrolic and hydrology:
            pass
        if not (hydrolic or hydrology):
            print("You have to give hyldrology or hydrolic !")

    def hydrology(self, **runoff_landa):
        self.output_hyrology = Map()

        if (runoff_landa.get("runoff_co_map", default=None) is None &
            runoff_landa.get("landa_map", default=None) is None):
            print("you have to give at least 1 map from runoff or landa !")
        else:
            if (runoff_landa.get("runoff_co_map", default=None) is not None) and (
                        runoff_landa.get("landa_map", default=None) is not None):
                runoff_coefficient_map_ascii = runoff_landa.get("runoff_co_map")
                self.landa_map = runoff_landa.get("landa_map")

                self.runoff_coefficient_map = map_loader.load_map(RunoffCoefficient, runoff_coefficient_map_ascii)
                runoff_coefficient_map = self.runoff_coefficient_map.map

                for i in range(len(self.runoff_coefficient_map.matrix)):
                    self.output_hyrology.matrix.append([])
                    for j in range(len(self.runoff_coefficient_map.matrix[i])):
                        if self.runoff_coefficient_map.matrix[i][j] != runoff_coefficient_map.no_data_value:
                            self.output_hyrology.matrix[i].append(
                                self.runoff_coefficient_map.matrix[i][j] + self.landa_map.matrix[i][j])
                        else:
                            self.output_hyrology.matrix[i].append(runoff_coefficient_map.no_data_value)

            else:
                if runoff_landa.get("runoff_co_map", default=None) is not None:
                    self.output_hyrology = self.runoff_coefficient_map
                if runoff_landa.get("landa_map", default=None) is not None:
                    self.output_hyrology = self.landa_map

        return self.output_hyrology

    def hydrolic(self, rpt_file, link_col_name, limit_node, limit=1, sub_dic=None):
        # sub_dic format : { 'region':[sub1_id , sub2_id , ... ] , 'region2' : [sub1_id , sub2_id , ... ] , ...  }
        """
        :type sub_dic: dict
        """
        result = []

        if sub_dic is None:
            sub_dic = {}

        #print os.getcwd()
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

        for i in range(5):
            Node_FS.pop()

        Nodes = []
        for i in range(len(Node_FS)):
            if int(Node_FS[i][0]) <= int(limit_node):
                Nodes.append(Node_FS[i][0])



            # ---- Find Link Flow Summary ------
        check = True
        while check:
            l = rpt.readline()
            if "Link Flow Summary" in l:
                check2 = True
                while check2:
                    l = rpt.readline()
                    if "Link" in l:
                        l = rpt.readline()
                        l = rpt.readline()

                        check3 = True
                        while check3:
                            if "*" in l:
                                check3 = False

                            # mem.append(l)
                            l += rpt.readline()

                        check = False
                        check2 = False

        rpt.close()

        Link_FS = []
        a = l.split("\n")
        for i in range(len(a)):
            Link_FS.append([])
            l = str(a[i])
            a[i] = l.split(" ")
            for j in a[i]:
                if j != '':
                    Link_FS[i].append(j)

        for i in range(5):
            Link_FS.pop()

        pipes = []

        if link_col_name == "MAX/FULL FLOW":
            for i in range(len(Link_FS)):
                if len(Link_FS[i]) == 8:
                    if float(Link_FS[i][6]) >= float(limit):
                        # print (float(Link_FS[i][6]))
                        pipes.append(Link_FS[i][0])

        # now we have : Nodes[]    -> that has regions
        #               pipes[]  -> that has pipes

        for i in sub_dic.keys():
            if not (str(i) in Nodes):
                for j in sub_dic.get(i):
                    #for k in range(len(Node_FS)):
                    if j in pipes:
                        result.append(i)

        for i in Nodes:
            result.append(i)

        print "Nodes:", Nodes
        print "pipes:", pipes
        print "result:", result

        result.sort()
        result = list(set(result))


        return result

    def build_basic_output_for_watershell(self):
        for i in range(self.output_for_watershell.n_rows):
            self.output_for_watershell.matrix.append([])
            for j in range(self.output_for_watershell.n_cols):
                self.output_for_watershell.matrix[i].append(self.output_for_watershell.no_data_value)

    def build_graph_by_inp_file(self, inp_file_name):
        rpt = open(inp_file_name, "r")
        while True:
            line = rpt.readline()
            if "[CONDUITS]" in line:
                rpt.readline()
                rpt.readline()
                data_line = ""
                while True:
                    line = rpt.readline()
                    if "[PUMPS]" in line:
                        break
                    data_line += line
                break
        lines = data_line.split("\n")
        basic_node = []
        for i in range(len(lines)):
            basic_node.append([])
            lines[i] = str(lines[i]).split(" ")
            for j in lines[i]:
                if j != '':
                    basic_node[i].append(j)
        graph = {}
        for n in basic_node:
            if len(n) == 9:
                n[1] = int(n[1])
                n[2] = int(n[2])
                if graph.get(n[2]) is None:
                    graph[n[2]] = []
                graph[n[2]].append({"node": n[1], "edge": n[0]})
        return graph

    def build_sub_dicts_by_inp_file(self, inp_file_name, limit_node, merge_nodes=None):
        limit_node = int(limit_node)
        #   merge_nodes format: {1: [1,2,3], 2: [5], 6: [6]} (always None)
        self.graph = self.build_graph_by_inp_file(inp_file_name)
        self.main_node_to_edges = {i: [] for i in range(1, limit_node + 1)}
        for main_node in self.main_node_to_edges:
            self.append_new_pipes_to_main_node_from_node(main_node, main_node, limit_node)
        if merge_nodes is None:
            return self.main_node_to_edges
        merge_node_to_edges = {node: [] for node in merge_nodes}
        for new_node in merge_nodes:
            old_nodes = merge_nodes[new_node]
            for old_node in old_nodes:
                merge_node_to_edges[new_node].extend(self.main_node_to_edges[old_node])
        return merge_node_to_edges


    def append_new_pipes_to_main_node_from_node(self, main_node, n1, limit_node):
        if n1 <= limit_node and n1 != main_node:
            return
        for edge in self.graph.get(n1, []):
            pipe = edge["edge"]
            n2 = edge["node"]
            if pipe not in self.main_node_to_edges[main_node]:
                self.main_node_to_edges[main_node].append(pipe)
            self.append_new_pipes_to_main_node_from_node(main_node, n2, limit_node)

    def build_watershed_map_based_on_merge_nodes(self, watershed_map_name, merge_nodes):
        old_watershed = map_loader.load_map(WaterShellMap, watershed_map_name)
        old_map = old_watershed.map
        new_map = copy.deepcopy(old_map)
        for i in range(len(old_map.matrix)):
            for j in range(len(old_map.matrix[i])):

                cell = int(old_map.matrix[i][j])
                if cell > 0:
                    new_map.matrix[i][j] = merge_nodes[cell - 1]



        return new_map

    def build_output_based_on_hydrolic(self, water_shell_map_ascii_name,
                                       rpt_file,
                                       link_col_name,
                                       limit_node,
                                       inp_file_name,
                                       limit=1,
                                       merge_nodes=None):
        #   merge_nodes format: [1, 1, 1, 2, 3, 5, 4, 6, 7]
        #   it means: 1 , 2 , 3 -> 1 & 4 -> 2 , 5 -> 3 , 6 -> 5 , 7 -> 4 , 8 -> 6 , 9 -> 7
        sub_dic = self.build_sub_dicts_by_inp_file(inp_file_name, limit_node, None)
        data_list = self.hydrolic(rpt_file, link_col_name, limit_node, limit, sub_dic)
        for i in range(len(data_list)):
            data_list[i] = int(data_list[i])
        water_shed_map = self.build_watershed_map_based_on_merge_nodes(water_shell_map_ascii_name, merge_nodes)
        #water_shed_m = water_shed_map.map
        water_shed_m = water_shed_map
        self.output_for_watershell = Map()
        self.output_for_watershell.set_config(water_shed_m)
        self.build_basic_output_for_watershell()
        for i in range(len(water_shed_m.matrix)):
            for j in range(len(water_shed_m.matrix[i])):
                pixel = water_shed_m.matrix[i][j]
                if pixel == water_shed_m.no_data_value:
                    continue
                if pixel in data_list:
                    #print("pixel in data list:", pixel)
                    self.output_for_watershell.matrix[i][j] = 1
                else:
                    self.output_for_watershell.matrix[i][j] = 0
        return self.output_for_watershell

#print(HighPotentialArea(hydrolic=True).hydrolic("report.rpt", "MAX/FULL FLOW", "32", "1.2", {'10': ['43544', '43546']}))
# a = HighPotentialArea(hydrolic=True)
# b = a.build_output_based_on_hydrolic("watershed.asc", "report.rpt", "MAX/FULL FLOW", "32",  "tmp.inp", "1.6")
# b.to_file("hydrolical.asc")
# b = a.build_sub_dicts_by_inp_file("tmp.inp", 31,  {1:[1,2], 2:[3,4,5], 3:[8]})
# for i in b:
#     print("main node:", i, "__pipes:", b[i])