from model import Vec2Int, EntityAction, MoveAction, AttackAction, AutoAttack


class ArmyDefensiveStrategy:
    def __init__(self, enemies_detector_type, gathering_point):
        self.__enemies_detector = enemies_detector_type
        self.__gathering_point = gathering_point

    def update(self, army, allies, enemies, commands):
        enemies_detector = self.__enemies_detector()
        enemies_detector.check_collisions(allies, enemies)
        detected_enemies = enemies_detector.get_collisions()
        detected_enemies_count = len(detected_enemies)

        if detected_enemies_count <= 0:
            self.move_to_gathering_point(army, commands)
        else:
            self.attack_enemies(army, list(detected_enemies), commands)

    def move_to_gathering_point(self, army, commands):
        for unit in army.get_ranged_units():
            self.move_to(unit, self.__gathering_point, commands)
        for unit in army.get_melee_units():
            self.move_to(unit, Vec2Int(self.__gathering_point.x + 3, self.__gathering_point.y + 3), commands)

    def move_to(self, unit, gathering_point, commands):
        commands.entity_actions[unit] = EntityAction(MoveAction(gathering_point, True, True), None,
                                                     AttackAction(None, AutoAttack(5, [])), None)

    def attack_enemies(self, army, detected_enemies, commands):
        for unit in enumerate(army.get_melee_units() + army.get_ranged_units()):
            self.send_intercepting_unit(detected_enemies[unit[0] % len(detected_enemies)], unit[1], commands)

    def send_intercepting_unit(self, enemy, unit, commands):
        commands.entity_actions[unit] = EntityAction(MoveAction(enemy.position, True, True), None,
                                                        AttackAction(enemy.id, AutoAttack(5, [])), None)