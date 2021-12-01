from model import EntityType, EntityAction, MoveAction, AttackAction, AutoAttack, Vec2Int


class BuilderUnitsDirector:
    def __init__(self, units, units_tracker):
        self.__units = units
        self.__units_tracker = units_tracker

    def update_commands(self, commands, map_size, builder_properties):
        for unit in filter(lambda item: item.entity_type == EntityType.BUILDER_UNIT, self.__units):
            self.send_for_resources(unit, commands, map_size, builder_properties)

    def send_for_resources(self, unit, commands, map_size, builder_properties):
        if not self.__units_tracker.is_unit_idle(unit):
            return

        move_action = MoveAction(Vec2Int(map_size - 1, map_size - 1), True, True)
        attack_action = AttackAction(None, AutoAttack(builder_properties.sight_range, [EntityType.RESOURCE]))
        commands.entity_actions[unit.id] = EntityAction(move_action, None, attack_action, None)
