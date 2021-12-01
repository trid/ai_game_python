from model import MoveAction, EntityAction, AutoAttack, AttackAction


class AttackAll:
    def __init__(self, unit, targets_position, targets_types, prioritized):
        self.__unit_id = unit.id
        self.__targets_position = targets_position
        self.__targets_types = targets_types
        self.__prioritized = prioritized

    def update(self, player_view, commands):
        move_action = MoveAction(self.__targets_position, True, True)
        auto_attack = AutoAttack(5, self.__targets_types[:1] if self.__prioritized else self.__targets_types)
        attack_action = AttackAction(None, auto_attack)
        commands.entity_actions[self.__unit_id] = EntityAction(move_action, None, attack_action, None)

    def finished(self, player_view):
        entities = list(filter(lambda item: item.id == self.__unit_id, player_view.entities))
        return len(entities) == 0
