from model import EntityType, EntityAction, MoveAction, AttackAction, AutoAttack


class BattleUnitsDirector:
    def __init__(self, units, units_tracker):
        self.__units = units
        self.__units_tracker = units_tracker

    def update_commands(self, detected_enemies, commands):
        for enemy in detected_enemies:
            self.send_intercepting_units(enemy, commands)

    def send_intercepting_units(self, enemy, commands):
        attackers_count = 0
        for unit in self.__units:
            if unit.entity_type != EntityType.MELEE_UNIT and unit.entity_type != EntityType.RANGED_UNIT:
                continue

            if self.__units_tracker.is_unit_idle(unit):
                attackers_count += 1
                self.__units_tracker.set_unit_working(unit)
                commands.entity_actions[unit.id] = EntityAction(MoveAction(enemy.position, True, True), None,
                                                                AttackAction(enemy.id, AutoAttack(5, [])), None)
                if attackers_count >= 2:
                    return
