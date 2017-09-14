import os

# pre =
# ncols         1852
# nrows         1613
# xllcorner     150257.4383344
# yllcorner     164583
# cellsize      2
# NODATA_value  -9999
from lib2to3.pgen2.grammar import line


class Map2Asc:
    def  __init__(self):
        self.ncols        = 1852
        self.nrows        = 1613
        self.xllcorner    = 150257.4383344
        self.yllcorner    = 164583
        self.cellsize     = 2
        self.NODATA_VALUE = -9999

    def set_map_variables(self, vars: dict):
        self.ncols = vars.get('ncols', 1852)
        self.nrows = vars.get('nrows', 1613)
        self.xllcorner = vars.get('xllcorner', 150257.4383344)
        self.yllcorner = vars.get('yllcorner', 164583)
        self.cellsize = vars.get('cellsize', 2)
        self.NODATA_VALUE = vars.get('NODATA_VALUE', -9999)

    def build_ascii_map(self, map_dir , map_name , ascii_name):
        os.chdir(map_dir)
        # os.chdir("D:\\Python_Proj\\water-engineering\\maps")
        os.system("map2asc -m -9999 " +  map_name+" " +ascii_name)

        a = open(ascii_name , "r")
        s = a.read()
        a.close()
        a = open(ascii_name  , "w")
        #a.write(str(self.ncols) + "\n" + str(self.nrows )+  "\n" + str(self.xllcorner )+ "\n" + str(self.yllcorner) + "\n" + str(self.cellsize )+ "\n" + str(self.NODATA_VALUE)+ "\n" )
        a.write("ncols         1852\nnrows         1613\nxllcorner     150257.4383344\nyllcorner     164583\ncellsize      2\nNODATA_value  -9999\n")
        a.write(s)
        a.close()

e = Map2Asc()

e.build_ascii_map("maps\\" , "slope.map" , "tt.asc")
