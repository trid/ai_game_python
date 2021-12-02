from enum import IntEnum

from model import EntityType


def square_distance(x1, x2, y1, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    return delta_x * delta_x + delta_y * delta_y


class DetectionStrategy(IntEnum):
    BY_BUILDINGS_AND_BUILDERS = 0,
    BY_ALL_ENTITES = 1


class EnemiesDetector:
    DANGEROUS_DISTANCE_SQ = 400

    def __init__(self, detection_strategy):
        self.__collisions = set()
        self.__detection_strategy = detection_strategy

    def check_collisions(self, allies, enemies):
        building_and_builders_types = (
                                       EntityType.RANGED_BASE, EntityType.MELEE_BASE, EntityType.BUILDER_BASE,
                                       EntityType.TURRET, EntityType.BUILDER_UNIT)
        detecting_units = allies if self.__detection_strategy == DetectionStrategy.BY_ALL_ENTITES else list(
            filter(lambda entity: entity.entity_type in building_and_builders_types, allies))
        for unit in detecting_units:
            self.find_all_collisions(unit, enemies)

    def find_all_collisions(self, unit, enemies):
        for enemy in enemies:
            sq_dist = square_distance(unit.position.x, enemy.position.x, unit.position.y, enemy.position.y)
            if (sq_dist < self.DANGEROUS_DISTANCE_SQ):
                self.__collisions.add(enemy)

    def get_collisions(self):
        return self.__collisions
