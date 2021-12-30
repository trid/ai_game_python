from decider.army.army import Army
from decider.army.army_defensive_strategy import ArmyDefensiveStrategy
from decider.army.army_updater import ArmyUpdater
from decider.army.default_assigning_strategy import DefaultAssigningStrategy
from decider.enemies_detector import EnemiesDetector
from model import Vec2Int


class ArmyTactics:
    def __init__(self, units_tracker):
        self.__units_tracker = units_tracker
        self.__attacking_armies = []
        self.__defending_army = Army(20, 20)
        self.__strategy = ArmyDefensiveStrategy(EnemiesDetector, Vec2Int(10, 10))
        self.__army_updater = ArmyUpdater([self.__defending_army], self.__units_tracker, DefaultAssigningStrategy())

    def update(self, result, units_storage):
        self.__army_updater.update(units_storage.get_allies())
        for army in self.__attacking_armies:
            self.__strategy.update(army, units_storage.get_allies(), units_storage.get_enemies(), result)
        self.__strategy.update(self.__defending_army, units_storage.get_allies(), units_storage.get_enemies(), result)
        if self.__defending_army.is_filled():
            self.__attacking_armies.append(self.__defending_army)
            self.__defending_army.set_limits(0, 0)
            self.__defending_army = Army(20, 20)
            self.__army_updater.add_army(self.__defending_army)
