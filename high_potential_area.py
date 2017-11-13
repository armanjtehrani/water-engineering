from algorithms import *
from maps import Map


class HighPotentialArea:
    def __init__(self, hydrology=False, hydrolic=False, **runoff_landa):

        if (hydrology == True):
            hydrology(self, **runoff_landa)
        if (hydrolic == True):
            pass
        if (hydrolic and hydrology):
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
                        if (self.runoff_coefficient_map.matrix[i][j] != runoff_coefficient_map.no_data_value):
                            self.output_hyrology.matrix[i].append(
                                self.runoff_coefficient_map.matrix[i][j] + self.landa_map.matrix[i][j])
                        else:
                            self.output_hyrology.matrix[i].append(runoff_coefficient_map.no_data_value)

            else:
                if (runoff_landa.get("runoff_co_map", default=None) is not None):
                    self.output_hyrology = self.runoff_coefficient_map
                if ((runoff_landa.get("landa_map", default=None) is not None)):
                    self.output_hyrology = self.landa_map

        return self.output_hyrology

    def hydrolic(self, rpt_file , col_name , limit):

        rpt = open(rpt_file, "r")
        mem = []

        check = True
        while(check):
            l = rpt.readline()
            if ("Link Flow Summary" in l):
                check2 = True
                while(check2):
                    l = rpt.readline()
                    if("Link" in l):
                        l = rpt.readline()
                        l = rpt.readline()

                        check3 = True
                        while (check3):
                            if("*" in l):
                                check3 = False

                            #mem.append(l)
                            l += rpt.readline()

                        check = False
                        check2= False

        rpt.close()

        table=[]
        a = l.split("\n")
        for i in range(len(a)):
            table.append([])
            l = str(a[i])
            a[i] = l.split(" ")
            for j in a[i]:
                if j !='':
                    table[i].append(j)

        for i in range(5):
            table.pop()
        
        links = []
        
        if (col_name == "MAX/FULL FLOW"):
            for  i in range(len(table)):
                if (len(table[i])==8):
                    if float(table[i][6])>= float(limit):
                        #print (float(table[i][6]))
                        links.append(table[i][0])

        return links


a = HighPotentialArea(hydrolic=True).hydrolic("report.rpt","MAX/FULL FLOW","0.2")

