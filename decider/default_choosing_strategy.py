from decider.constants import STARTING_POPULATION_LIMIT, HOUSE_INITIAL_COST, MELEE_INITIAL_COST, \
    RANGED_INITIAL_COST, BUILDER_INITIAL_COST, NEED_MORE_POPULATION_COEFFICIENT, MAX_BUILDERS_COUNT
from model.entity_type import EntityType


class DefaultChoosingStrategy:
    def __init__(self, builder_to_archers_proportion=1.5, archers_to_melee_proportion=2):
        self.__builder_to_archers_proportion = builder_to_archers_proportion
        self.__archers_to_melee_proportion = archers_to_melee_proportion

    @staticmethod
    def count_penalty(count):
        return count * (count - 1) / 2

    def decide(self, units_storage, entities_params, current_resources, houses_requested):
        builders_count = 0
        melee_count = 0
        range_count = 0
        houses_count = 0
        population_limit = STARTING_POPULATION_LIMIT
        result = []

        for item in units_storage.get_allies():
            if item.entity_type == EntityType.BUILDER_UNIT:
                builders_count += 1
            elif item.entity_type == EntityType.MELEE_UNIT:
                melee_count += 1
            elif item.entity_type == EntityType.RANGED_UNIT:
                range_count += 1
            elif item.entity_type == EntityType.HOUSE:
                if item.health == 50:
                    houses_count += 1

        population_limit = STARTING_POPULATION_LIMIT + entities_params[EntityType.HOUSE].population_provide * (houses_count + houses_requested)

        # Resources for the requested houses
        current_resources -= houses_requested * HOUSE_INITIAL_COST + self.count_penalty(houses_count + houses_requested)

        # Do we need more houses?
        if builders_count + melee_count + range_count >= population_limit * NEED_MORE_POPULATION_COEFFICIENT and \
                current_resources > HOUSE_INITIAL_COST:
            print("Population limit reached: produce houses")
            current_resources -= HOUSE_INITIAL_COST
            result.append(EntityType.HOUSE)

        # What is it for?
        elif builders_count == 0:
            builders_count += 1
            result.append(EntityType.BUILDER_UNIT)
        elif range_count == 0:
            range_count += 1
            result.append(EntityType.RANGED_UNIT)
        elif melee_count == 0:
            melee_count += 1
            result.append(EntityType.MELEE_UNIT)

        # Actually, with Python3 we don't need such precaution, but I believe there would be problems with Python2
        # Better safe than sorry

        # if float(builders_count) / range_count < self.__builder_to_archers_proportion and \
        if builders_count < MAX_BUILDERS_COUNT and current_resources - BUILDER_INITIAL_COST - self.count_penalty(builders_count) >= 0:
            builders_count += 1
            current_resources = current_resources - BUILDER_INITIAL_COST - self.count_penalty(builders_count)
            result.append(EntityType.BUILDER_UNIT)
        if float(range_count) / melee_count < self.__archers_to_melee_proportion and \
                current_resources - RANGED_INITIAL_COST - self.count_penalty(range_count) >= 0:
            current_resources = current_resources - RANGED_INITIAL_COST - self.count_penalty(range_count)
            result.append(EntityType.RANGED_UNIT)
        if current_resources - MELEE_INITIAL_COST - self.count_penalty(melee_count) >= 0:
            result.append(EntityType.MELEE_UNIT)
            current_resources -= MELEE_INITIAL_COST - self.count_penalty(melee_count)

        return result
