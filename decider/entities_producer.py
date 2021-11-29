from decider.unit_builder import UnitBuilder
from model import EntityType


class EntitiesProducer:
    def __init__(self, choosing_strategy):
        self.__choosing_strategy = choosing_strategy

    def update(self, commands, units_storage, entities_params):
        entity_to_produce = self.__choosing_strategy.decide(units_storage, entities_params)
        self.produce_entity(entity_to_produce, entities_params, commands, units_storage.get_allies())

    def produce_entity(self, entity_type, building_params, commands, units):
        melee_unit_builder = UnitBuilder(EntityType.MELEE_BASE, building_params[EntityType.MELEE_BASE], units)
        melee_unit_builder.stop(commands)
        range_unit_builder = UnitBuilder(EntityType.RANGED_BASE, building_params[EntityType.RANGED_BASE], units)
        range_unit_builder.stop(commands)
        builders_unit_builder = UnitBuilder(EntityType.BUILDER_BASE, building_params[EntityType.BUILDER_BASE], units)
        builders_unit_builder.stop(commands)

        if entity_type == EntityType.MELEE_UNIT:
            melee_unit_builder.build_unit(commands)
        elif entity_type == EntityType.RANGED_UNIT:
            range_unit_builder.build_unit(commands)
        elif entity_type == EntityType.BUILDER_UNIT:
            builders_unit_builder.build_unit(commands)
        elif entity_type == EntityType.HOUSE:
            # Build houses here
            pass
        else:
            print("Decided to produce nothing? Oh well.")
