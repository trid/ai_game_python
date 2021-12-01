from decider.units_tracker import UnitsTracker
from model import EntityType, EntityAction, MoveAction, AttackAction, AutoAttack


class DefensiveBattleUnitsDirector:
    def __init__(self, units, units_tracker):
        self.__units_tracker = units_tracker
        self.__units = list(filter(self.__filter_units, units))
        self.__internal_tracker = UnitsTracker()

    def __filter_units(self, unit):
        return unit.entity_type == EntityType.MELEE_UNIT or unit.entity_type == EntityType.RANGED_UNIT or \
               not self.__units_tracker.is_unit_idle(unit)

    def update_commands(self, detected_enemies, commands):
        for enemy in detected_enemies:
            self.send_intercepting_units(enemy, commands, len(self.__units) / len(detected_enemies))

    def send_intercepting_units(self, enemy, commands, units_per_enemy):
        attackers_count = 0
        for unit in self.__units:
            if self.__internal_tracker.is_unit_idle(unit):
                attackers_count += 1
                commands.entity_actions[unit.id] = EntityAction(MoveAction(enemy.position, True, True), None,
                                                                AttackAction(enemy.id, AutoAttack(5, [])), None)
                if attackers_count >= units_per_enemy:
                    return
