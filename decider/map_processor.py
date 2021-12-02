from model.player_view import PlayerView
from decider.constants import BUILDING_BASE_SIZE, BUILDING_HOUSE_SIZE, BUILDING_TURRET_SIZE
from model import EntityType


class MapProcessor:
    def __init__(self, player_view):
        self.__map = {}

        for entity in player_view.entities:
            entity_size = (1, 1)
            if entity.entity_type == EntityType.HOUSE:
                entity_size = BUILDING_HOUSE_SIZE
            elif (entity.entity_type == EntityType.BUILDER_BASE) or \
                    (entity.entity_type == EntityType.MELEE_BASE) or \
                    (entity.entity_type == EntityType.RANGED_BASE):
                entity_size = BUILDING_BASE_SIZE
            elif entity.entity_type == EntityType.TURRET:
                entity_size = BUILDING_TURRET_SIZE

            for x in range(entity.position.x, entity.position.x + entity_size[0]):
                for y in range(entity.position.y, entity.position.y + entity_size[1]):
                    self.__map[x, y] = entity

    def get_map(self):
        return self.__map
