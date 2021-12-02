from decider.constants import HOUSE_BUILDERS, BUILDING_HOUSE_SIZE
from model import BuildAction, MoveAction, RepairAction, Vec2Int, EntityAction, EntityType


class HouseBuilder:
    def __init__(self):
        self.__builders_id = []
        self.__house_builder_counts = HOUSE_BUILDERS
        self.__houses = 0
        self.__house_are_building = False
        self.__update_build_commands = {}
        self.__update_repair_commands = {}
        self.__buided_houses = []

    def update(self, units):
        houses = list(filter(lambda item: item.entity_type == EntityType.HOUSE, units))
        if len(houses) == 0:
            return

        for house in houses:
            if house.health < 50:
                repair_action = RepairAction(house.id)
                self.__update_repair_commands[self.__builders_id[0]] = EntityAction(None, None, None, repair_action)
                self.__update_build_commands[self.__builders_id[0]] = None
            elif house.id not in self.__buided_houses:
                self.__buided_houses.append(house.id)
                self.__update_repair_commands[self.__builders_id[0]] = None
                self.__builders_id.pop(0)
                self.__house_are_building = False

    def update_commands(self, commands):
        for id, command in self.__update_build_commands.items():
            if command is not None:
                commands.entity_actions[id] = command
                print("Build house = ", id, " coord=", command)

        for id, command in self.__update_repair_commands.items():
            if command is not None:
                commands.entity_actions[id] = command
                print("Repair house = ", id)

    def is_builder(self, id):
        if id in self.__builders_id:
            return True

    def print_builders(self):
        print(self.__builders_id)

    def add_house(self, commands_list, current_map, units):
        if self.__house_are_building:
            return

        self.__house_are_building = True

        house_coord = self.get_new_house_coors(current_map)
        self.__houses += 1

        builder_id = self.find_nearest_builder_id(house_coord, units)

        build_action = BuildAction(
            EntityType.HOUSE,
            Vec2Int(house_coord[0], house_coord[1]))

        move_action = MoveAction(
            Vec2Int(house_coord[0], house_coord[1]),
            False,
            False)

        self.__builders_id.append(builder_id)
        commands_list.entity_actions[builder_id] = EntityAction(move_action, build_action, None, None)

        self.__update_build_commands[builder_id] = EntityAction(move_action, build_action, None, None)

        print("House coord=", house_coord, " builder_id=", builder_id)

    def check_if_suitable_position(self, current_map, coord):
        for x in range(coord[0] - 1, coord[0] + BUILDING_HOUSE_SIZE[0] + 1):
            for y in range(coord[1] - 1, coord[1] + BUILDING_HOUSE_SIZE[1] + 1):
                if current_map.get((x, y)) is not None:
                    return False

        return True

    def get_new_house_coors(self, current_map):
        map_for_houses_size = 50
        distance_from_the_corner = 0

        while distance_from_the_corner < map_for_houses_size:
            for x in range(distance_from_the_corner):
                y = distance_from_the_corner - x
                if self.check_if_suitable_position(current_map, (x, y)):
                    print("NEW HOUSE SUITABLE: ", (x, y))
                    return x, y

            distance_from_the_corner += 1

    def find_nearest_builder_id(self, house_coord, units):
        buildings = list(filter(lambda item: item.entity_type == EntityType.BUILDER_UNIT, units))
        if len(buildings) == 0:
            return
        # get first
        return buildings[0].id