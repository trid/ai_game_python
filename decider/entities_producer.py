from decider.constants import MAX_HOUSES_PER_TICK
from decider.unit_builder import UnitBuilder
from model import EntityType


class EntitiesProducer:
    def __init__(self, choosing_strategy, current_map, house_builder):
        self.__choosing_strategy = choosing_strategy
        self.__map = current_map
        self.__house_builder = house_builder
        self.__house_number = 0

    def update(self, commands, units_storage, entities_params, current_resources):
        entities_to_produce = self.__choosing_strategy.decide(units_storage, entities_params, current_resources)
        self.produce_entity(entities_to_produce, entities_params, commands, units_storage.get_allies())

    def produce_entity(self, produced_entities, building_params, commands, units):
        melee_unit_builder = UnitBuilder(EntityType.MELEE_BASE, building_params[EntityType.MELEE_BASE], units)
        melee_unit_builder.stop(commands)
        range_unit_builder = UnitBuilder(EntityType.RANGED_BASE, building_params[EntityType.RANGED_BASE], units)
        range_unit_builder.stop(commands)
        builders_unit_builder = UnitBuilder(EntityType.BUILDER_BASE, building_params[EntityType.BUILDER_BASE], units)
        builders_unit_builder.stop(commands)

        for entity_type in produced_entities:
            if entity_type == EntityType.MELEE_UNIT:
                melee_unit_builder.build_unit(commands, self.__map)
            elif entity_type == EntityType.RANGED_UNIT:
                range_unit_builder.build_unit(commands, self.__map)
            elif entity_type == EntityType.BUILDER_UNIT:
                builders_unit_builder.build_unit(commands, self.__map)
            elif entity_type == EntityType.HOUSE:
                if self.__house_number < MAX_HOUSES_PER_TICK:
                    self.__house_builder.add_house(commands, self.__map, units)
                    self.__house_number += 1
