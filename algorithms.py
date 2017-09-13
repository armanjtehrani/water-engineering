from map_loader import MapLoader
from maps import Map
from maps import GWMap
from maps import SoilMap
from maps import LandUseMap


map_loader = MapLoader()


class SuitableAreaBasedOnGW:
    def get_suitable_areas(self, GW_ascii_map_name, user_limit):
        self.gw_map = map_loader.load_map(GWMap, GW_ascii_map_name)
        self.output = Map()
        self.output.set_config(self.gw_map.map)
        # self.output.no_data_value = 0
        for i in range(len(self.gw_map.map.matrix)):
            self.output.matrix.append([])
            for pixel in self.gw_map.map.matrix[i]:
                if pixel > user_limit:
                    self.output.matrix[i].append(0)
                elif pixel == self.gw_map.map.no_data_value:
                    self.output.matrix[i].append(self.output.no_data_value)
                else:
                    self.output.matrix[i].append(1)
        return self.output


class SuitableSoilArea:
    def get_suitable_areas(self, soil_ascii_map_name, landuse_ascii_map_name, user_soil_number):
        self.soil_map = map_loader.load_map(SoilMap, soil_ascii_map_name)
        self.landuse_map = map_loader.load_map(LandUseMap, landuse_ascii_map_name)
        self.output = Map()
        self.output.set_config(self.soil_map.map)
        for i in range(len(self.soil_map.map.matrix)):
            self.output.matrix.append([])
            for j in range(len(self.soil_map.map.matrix[i])):
                if self.soil_map.map.matrix[i][j] == self.soil_map.map.no_data_value:
                    self.output.matrix[i].append(self.output.no_data_value)
                elif self.soil_map.map.matrix[i][j] != user_soil_number:
                    # print('yes baby')
                    self.output.matrix[i].append(0)
                elif self.landuse_map.map.matrix[i][j] == LandUseMap.VALUES.URBON_AND_BUILT_UP or \
                        self.landuse_map.map.matrix[i][j] == LandUseMap.VALUES.WATER_BODIES:
                    # print('i\'ll cum in ur face')
                    self.output.matrix[i].append(0)
                else:
                    self.output.matrix[i].append(1)
        return self.output