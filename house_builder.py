from model.player_view import PlayerView
import constants


class HouseBuilder:
    def __init__(self):
        self.__builders_id = []
        self.__house_builder_counts = constants.HOUSE_BUILDERS
        self.__houses = 0
        self.__coord = ()

    def add_builders(self, id):
        self.__builders_id.append(id)

    def is_builder(self, id):
        if id in self.__builders_id:
            return True

    def print_builders(self):
        print(self.__builders_id)

    def add_house(self, coord):
        self.__houses =+1
        self.__coord = coord

    def get_houses_count(self):
        return self.__houses

    def get_house_coord(self):
        return self.__coord