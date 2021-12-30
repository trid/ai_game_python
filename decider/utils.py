from model import EntityType


def find_idle_military_units(units, units_tracker):
    def is_military(unit):
        return unit.entity_type == EntityType.MELEE_UNIT or unit.entity_type == EntityType.RANGED_UNIT
    return list(filter(lambda unit: is_military(unit) and units_tracker.is_unit_idle(unit), units))


def find_units_by_types(units, types):
    return list(filter(lambda unit: unit.entity_type in types, units))


def find_unit_coordinates(unit_id, map):
    for coord, entity in map.items():
        if entity.id == unit_id:
            return coord

def manhattan_distance(point1, point2):
    return abs(point2.x - point1.x) + abs(point2.y - point1.y)