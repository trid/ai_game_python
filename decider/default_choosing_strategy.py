from decider.constants import STARTING_POPULATION_LIMIT
from model.entity_type import EntityType


class DefaultChoosingStrategy:
    def __init__(self, builder_to_archers_proportion=1.5, archers_to_melee_proportion=2):
        self.__builder_to_archers_proportion = builder_to_archers_proportion
        self.__archers_to_melee_proportion = archers_to_melee_proportion

    def decide(self, units_storage, entities_params):
        builders_count = 0
        melee_count = 0
        range_count = 0
        pop_limit = STARTING_POPULATION_LIMIT

        for item in units_storage.get_allies():
            if item.entity_type == EntityType.BUILDER_UNIT:
                builders_count += 1
            elif item.entity_type == EntityType.MELEE_UNIT:
                melee_count += 1
            elif item.entity_type == EntityType.RANGED_UNIT:
                range_count += 1
            elif item.entity_type == EntityType.HOUSE:
                pop_limit += entities_params[EntityType.HOUSE].population_provide

        if builders_count + melee_count + range_count >= pop_limit:
            print("Population limit reached: produce houses")
            return EntityType.HOUSE
        elif builders_count == 0:
            return EntityType.BUILDER_UNIT
        elif range_count == 0:
            return EntityType.RANGED_UNIT
        elif melee_count == 0:
            return EntityType.MELEE_UNIT
        # Actually, with Python3 we don't need such precaution, but I believe there would be problems with Python2
        # Better safe than sorry
        elif float(builders_count) / range_count < self.__builder_to_archers_proportion:
            return EntityType.BUILDER_UNIT
        elif float(range_count) / melee_count < self.__archers_to_melee_proportion:
            return EntityType.RANGED_UNIT
        return EntityType.MELEE_UNIT
