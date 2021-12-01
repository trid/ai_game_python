from model import MoveAction, EntityAction


class MoveTo:
    def __init__(self, unit, target):
        self.__unit_id = unit.id
        self.__target = target

    def update(self, player_view, commands):
        move_action = MoveAction(self.__target, True, True)
        commands.entity_actions[self.__unit_id] = EntityAction(move_action, None, None, None)

    def finished(self, player_view):
        entities = list(filter(lambda item: item.id == self.__unit_id, player_view.entities))
        # Surprisingly enough, there is no __eq__ method on Vec2Int
        return len(entities) == 0 or (
                    self.__target.x == entities[0].position.x and self.__target.y == entities[0].position.y)
