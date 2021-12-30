from enum import IntEnum

from decider.utils import manhattan_distance
from model import EntityType


class DetectionStrategy(IntEnum):
    BY_BUILDINGS_AND_BUILDERS = 0,
    BY_ALL_ENTITES = 1


class EnemiesDetector:
    DANGEROUS_DISTANCE = 20

    def __init__(self, detection_strategy=DetectionStrategy.BY_BUILDINGS_AND_BUILDERS):
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
            sq_dist = manhattan_distance(unit.position, enemy.position)
            if (sq_dist < self.DANGEROUS_DISTANCE):
                self.__collisions.add(enemy)

    def get_collisions(self):
        return self.__collisions
