from decider.units_tracker import UnitsTracker
from model import EntityType, EntityAction, MoveAction, AttackAction, AutoAttack


class DefensiveBattleUnitsDirector:
    def __init__(self, units, units_tracker):
        self.__units_tracker = units_tracker
        self.__units = list(filter(self.__filter_units, units))
        self.__internal_tracker = UnitsTracker()

    def __filter_units(self, unit):
        return (unit.entity_type == EntityType.MELEE_UNIT or unit.entity_type == EntityType.RANGED_UNIT) and \
               self.__units_tracker.is_unit_idle(unit)

    def update_commands(self, detected_enemies, commands):
        detected_enemies_count = len(detected_enemies)
        if detected_enemies_count == 0:
            return

        detected_enemies_list = list(detected_enemies)
        for unit in enumerate(self.__units):
            self.send_intercepting_unit(detected_enemies_list[unit[0] % detected_enemies_count], unit[1], commands)

    def send_intercepting_unit(self, enemy, unit, commands):
        commands.entity_actions[unit.id] = EntityAction(MoveAction(enemy.position, True, True), None,
                                                        AttackAction(enemy.id, AutoAttack(5, [])), None)
