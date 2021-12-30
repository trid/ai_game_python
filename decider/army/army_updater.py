from decider.utils import find_idle_military_units


class ArmyUpdater:
    def __init__(self, armies, units_tracker, units_assigning_strategy):
        self.__armies = armies
        self.__units_tracker = units_tracker
        self.__units_assigning_strategy = units_assigning_strategy

    def add_army(self, army):
        self.__armies.append(army)

    def update(self, units):
        for army in self.__armies:
            army.update(units)
        free_units = find_idle_military_units(units, self.__units_tracker)
        self.__units_assigning_strategy.assign(self.__armies, free_units, self.__units_tracker)