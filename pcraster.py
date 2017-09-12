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

    def build_ascii_map(self, map_dir:str , map_name:str , ascii_name:str):
        os.chdir(map_dir)
        # os.chdir("D:\\Python_Proj\\water-engineering\\maps")
        os.system("map2asc -m -9999 %s.map %s.asc" (map_name, ascii_name))



# print(os.getcwd())
os.chdir("D:\\Python_Proj\\water-engineering\\maps")
os.system("map2asc -m -9999 slope.map hi.asc")
#
