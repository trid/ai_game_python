from model import EntityType


def find_idle_military_units(units, units_tracker):
    def is_military(unit):
        return unit.entity_type == EntityType.MELEE_UNIT or unit.entity_type == EntityType.RANGED_UNIT
    return list(filter(lambda unit: is_military(unit) and units_tracker.is_unit_idle(unit), units))


def find_units_by_types(units, types):
    return list(filter(lambda unit: unit.entity_type in types, units))
