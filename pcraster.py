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
        self.NODATA_VALUE = vars.get('NODATA_value', -9999)

    def build_ascii_map(self, map_dir , map_name , ascii_name):
        os.chdir(map_dir)
        # os.chdir("D:\\Python_Proj\\water-engineering\\maps")
        os.system("map2asc -m -9999 " +  map_name+" " +ascii_name)
        a = open(ascii_name , "r")
        s = a.read()
        a.close()
        a = open(ascii_name  , "w")
        str_configs = self.get_config_in_str()
        # a.write(str_configs)
        a.write(s)
        a.close()

    def get_config_in_str(self):
        str_data = "ncols         " + str(self.ncols) + '\n'
        str_data += "nrows         "+ str(self.nrows) + '\n'
        str_data += "xllcorner     " + str(self.xllcorner) + '\n'
        str_data += "yllcorner     "+ str(self.yllcorner) + '\n'
        str_data += "cellsize      "+ str(self.cellsize) + '\n'
        str_data +=  "NODATA_value  " + str(self.NODATA_VALUE) + '\n'
        return str_data
a = Map2Asc()
map_name = "slope.map"
map_dir = "maps/"
ascii_name = map_name.split('.map')[0] + 'Cr.ascii'
configs = {
    'ncols': 23,
    'nrows': 243,
    'xllcorner': 32,
    'yllcorner': 332,
    'cellsize': 1212,
    'NODATA_value': 3232
}
a.set_map_variables(configs)
a.build_ascii_map(map_dir, map_name, ascii_name)
