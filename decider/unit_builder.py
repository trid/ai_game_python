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

    def build_unit(self, commands_list):
        if self.__building is None:
            # No producing building
            return

        build_action = BuildAction(
            self.__building_properties.build.options[0],
            Vec2Int(self.__building.position.x + self.__building_properties.size,
                    self.__building.position.y + self.__building_properties.size - 1))

        commands_list.entity_actions[self.__building.id] = EntityAction(None, build_action, None, None)

    def stop(self, commands_list):
        # "Горшочек не вари" mode
        commands_list.entity_actions[self.__building.id] = EntityAction(None, None, None, None)
