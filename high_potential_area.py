from algorithms import *
from maps import Map


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

        for i in sub_dic.keys():
            if not (i in Nodes):
                for j in sub_dic.get(i):
                    for k in range(len(Node_FS)):
                        if j == Node_FS[k][0]:
                            result.append(i)

        for i in Nodes:
            result.append(i)

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

        if link_col_name == "MAX/FULL FLOW":
            for i in range(len(Link_FS)):
                if len(Link_FS[i]) == 8:
                    if float(Link_FS[i][6]) >= float(limit):
                        # print (float(Link_FS[i][6]))
                        result.append(Link_FS[i][0])

        return result


print(HighPotentialArea(hydrolic=True).hydrolic("report.rpt", "MAX/FULL FLOW", "32", "1.6", {'10': ['43544', '43546']}))
