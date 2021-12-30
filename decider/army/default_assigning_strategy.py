from model import EntityType


class DefaultAssigningStrategy:
    def assign(self, armies, units, unit_tracker):
        for army in armies:
            requested_ranged, requested_melees = army.get_units_request()
            for unit in units:
                if unit.entity_type == EntityType.MELEE_UNIT and requested_melees > 0:
                    self.__add_unit_to_army(army, unit, unit_tracker)
                    requested_melees -= 1
                elif unit.entity_type == EntityType.RANGED_UNIT and requested_ranged > 0:
                    self.__add_unit_to_army(army, unit, unit_tracker)
                    requested_ranged -= 1
                else:
                    print("You really need to write some tests, man")

    def __add_unit_to_army(self, army, unit, unit_tracker):
        unit_tracker.set_unit_working(unit)
        army.add_unit(unit)