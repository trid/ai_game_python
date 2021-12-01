class UnitsTracker:
    def __init__(self):
        self.__working_units = set()

    def set_unit_working(self, unit):
        self.__working_units.add(unit.id)

    def set_unit_idle(self, unit):
        self.__working_units.remove(unit.id)

    def is_unit_idle(self, unit):
        return unit.id not in self.__working_units
