from model.entity_type import EntityType


class UnitsStorage:
    def __init__(self, player_id):
        self.__player_id = player_id
        self.__enemies = []
        self.__allies = []

    def update_storage(self, entities):
        for item in entities:
            if item.player_id == self.__player_id:
                self.__allies.append(item)
            elif item.entity_type != EntityType.RESOURCE:
                self.__enemies.append(item)

    def get_allies(self):
        return self.__allies

    def get_enemies(self):
        return self.__enemies
