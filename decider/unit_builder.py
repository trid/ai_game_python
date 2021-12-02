from model import BuildAction, Vec2Int, EntityAction


class UnitBuilder:
    def __init__(self, building_type, building_properties, units):
        self.__building_type = building_type
        self.__building_properties = building_properties
        self.__building = None

        buildings = list(filter(lambda item: item.entity_type == self.__building_type, units))
        if len(buildings) == 0:
            # There are no barracks, so we lost it, so we actually failed the game
            print("We failed :'(")
            return

        self.__building = buildings[0]

    def build_unit(self, commands_list, current_map):
        if self.__building is None:
            # No producing building
            return

        position_to_build = self.__find_empty_place_around(current_map)
        if position_to_build is None:
            print("No empty position around building")
            return

        build_action = BuildAction(
            self.__building_properties.build.options[0],
            Vec2Int(*position_to_build))

        commands_list.entity_actions[self.__building.id] = EntityAction(None, build_action, None, None)

    def stop(self, commands_list):
        if self.__building is None:
            return
        commands_list.entity_actions[self.__building.id] = EntityAction(None, None, None, None)

    def __find_empty_place_around(self, current_map):
        for pos in range(self.__building.position.x,
                           self.__building.position.x + self.__building_properties.size):
            point = (pos, self.__building.position.y - 1)
            if point[0] < 0 or point[1] < 0:
                continue
            # Search by x-axis
            if current_map.get(point, None) is None:
                return point
            point = (pos, self.__building.position.y + self.__building_properties.size)
            if current_map.get(point, None) is None:
                return point

        for pos in range(self.__building.position.y,
                           self.__building.position.y + self.__building_properties.size):
            point = (self.__building.position.x - 1, pos)
            if point[0] < 0 or point[1] < 0:
                continue
            # Search by x-axis
            if current_map.get(point, None) is None:
                return point
            point = (self.__building.position.x + self.__building_properties.size, pos)
            if current_map.get(point, None) is None:
                return point
        return None
