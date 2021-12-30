from model import EntityType


class Army:
    def __init__(self, ranged_count_max, melee_count_max):
        self.__ranged_count_max = ranged_count_max
        self.__melee_count_max = melee_count_max
        self.__melee_units = []
        self.__ranged_units = []

    def get_units_request(self):
        return self.__ranged_count_max - len(self.__ranged_units), self.__ranged_count_max - len(self.__ranged_units)

    def update(self, units):
        self.__melee_units = self.__update_melee_units(units)
        self.__ranged_units = self.__update_ranged_units(units)

    def __update_melee_units(self, units):
        return self.__update_units(units, self.__melee_units)

    def __update_ranged_units(self, units):
        return self.__update_units(units, self.__ranged_units)

    def __update_units(self, existing_units, army_units):
        ids = set(army_units)
        return list(filter(lambda x: x in ids, army_units))

    def get_melee_units(self):
        return self.__melee_units

    def get_ranged_units(self):
        return self.__ranged_units

    def add_unit(self, unit):
        if unit.entity_type == EntityType.MELEE_UNIT:
            self.__melee_units.append(unit.id)
        elif unit.entity_type == EntityType.RANGED_UNIT:
            self.__ranged_units.append(unit.id)
        else:
            print("WTF you're trying to append to army?")

    def is_filled(self):
        return len(self.__melee_units) >= self.__melee_count_max and len(self.__ranged_units) >= self.__ranged_count_max

    def set_limits(self, ranged_units, melee_units):
        self.__ranged_count_max = ranged_units
        self.__melee_units_max = melee_units
