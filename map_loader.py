import pcraster
from maps import Map, SoilMap, LandUseMap, ElevationMap


class MapLoader:
    def __init__(self):
        self.my_map2asc_convertor = pcraster.Map2Asc()
        self.configs = {
            'ncols': 1852,
            'nrows': 1613,
            'xllcorner': 150257.4383344,
            'yllcorner': 164583,
            'cellsize': 2,
            'NODATA_value': -9999
        }
        self.map_dir_for_ascii = "parammaps/"
        self.map_dir_for_dot_map = "parammaps/"

    def load_dot_map(self, map_class, map_name):
        map_dir = map_name
        if "/" in map_dir :
            a = map_dir.split("/")
            map_dir = map_dir.replace(a[len(a)-1],"")
            map_dir = map_dir[:len(map_dir)-1]
        elif "\\" in map_dir:
            a = map_dir.split("\\")

            map_dir = map_dir.replace(a[len(a)-1], "")
            map_dir = map_dir[:len(map_dir) - 1]
        else :
            map_dir = ""

        print map_dir
        ascii_name = map_name.split('.map')[0] + 'Cr.asc'
        #map_name = ascii_name.replace('Cr.asc',".map")

        print "map_name:",map_name
        print "ascii_name:",ascii_name

        print('asc name:', ascii_name)
        self.my_map2asc_convertor.set_map_variables(self.configs)
        self.my_map2asc_convertor.build_ascii_map(map_dir, map_name, ascii_name)
        return self.load_map(map_class, ascii_name)

    def load_map(self, map_class, map_name):
        map_file = self.load_file(map_name)
        map = self.build_map_from_ascii(map_file)
        self.set_my_map_config_by_map(map)
        my_map = map_class()
        my_map.map = map
        return my_map



    def load_file(self, map_name):
        # if (len(map_name)>20):
        #   return open(map_name, 'r')
        # else:
        #    return open(self.map_dir_for_ascii + map_name, 'r')
        return open(map_name, 'r')



    def build_map_from_ascii(self, ascii_file):
        map = Map()
        map.n_cols = int(ascii_file.readline().replace('ncols', '').replace('\n', ''))
        map.n_rows = int(ascii_file.readline().replace('nrows', '').replace('\n', ''))
        map.xll_corner = float(ascii_file.readline().replace('xllcorner', '').replace('\n', ''))
        map.yll_corner = float(ascii_file.readline().replace('yllcorner', '').replace('\n', ''))
        map.cell_size = int(ascii_file.readline().replace('cellsize', '').replace('\n', ''))
        map.no_data_value = int(ascii_file.readline().replace('NODATA_value', '').replace('\n', ''))
        #
        map.matrix = []
        for i in range(map.n_rows):
            line_str = ascii_file.readline().replace('\n', '')
            line_list = line_str.split(' ')
            while ('' in line_list):
                line_list.remove('')
            line_list = line_list[:len(line_list) - 1]

            for j in range(len(line_list)):
                ans = float(line_list[j])

                line_list[j] = ans

            if len(line_list) > map.n_cols:
                line_list = line_list[:map.n_cols]
            elif len(line_list) < map.n_cols:
                for j in range(map.n_cols - len(line_list)):
                    line_list.append(map.no_data_value)
            map.matrix.append(line_list)

        return map

    def set_my_map_config_by_map(self, map):
        self.configs['ncols'] = map.n_cols
        self.configs['nrows'] = map.n_rows
        self.configs['xllcorner'] = map.xll_corner
        self.configs['yllcorner'] = map.yll_corner
        self.configs['cellsize'] = map.cell_size
        self.configs['NODATA_value'] = map.no_data_value


class MapLoaderTester:
    def basic_test(self):
        t = MapLoader()
        m = t.load_map(ElevationMap, 'elevation.asc')
        print('m', m)

    def load_dot_map_test(self):
        a = MapLoader()
        t = a.load_dot_map(SoilMap, 'slope.map')
        print('tt: ', t)
