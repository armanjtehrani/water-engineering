import copy

from maps import Map, SoilMap, LandUseMap, ElevationMap


class MapLoader:
    def load_map(self, map_class,map_name):
        map_file = self.load_file(map_name)
        map = self.build_map_from_ascii(map_file)
        my_map = map_class()
        my_map.map = map
        return my_map

    def load_file(self, map_name):
        return open('maps/' + map_name, 'r')

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
            line_str = ascii_file.readline()
            line_list = line_str.split(' ')
            line_list = line_list[:len(line_list) - 1]

            for j in range(len(line_list)):
                line_list[j] = float(line_list[j])
            if len(line_list) > map.n_cols:
                line_list = line_list[:map.n_cols]
            elif len(line_list) < map.n_cols:
                for j in range(map.n_cols - len(line_list)):
                    line_list.append(map.no_data_value)
            map.matrix.append(line_list)
        return map

class MapLoaderTester:
    def basic_test(self):
        t = MapLoader()
        m = t.load_map(ElevationMap, 'elevation.asc')
        # print('m', m)