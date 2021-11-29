from model.player_view import PlayerView

class MapProcessor:
    def __init__(self, player_view):
        self.__map = {}

        for entity in player_view.entities:
            self.__map[(entity.position.x, entity.position.y)] = entity

    def get_map(self):
        return self.__map