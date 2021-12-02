from decider.builder_hunting_units_director import BuilderHuntingUnitsDirector
from decider.constants import ZERG_RUSH_READY_AMOUNT
from decider.defencive_battle_units_director import DefensiveBattleUnitsDirector
from decider.builder_units_director import BuilderUnitsDirector
from decider.default_choosing_strategy import DefaultChoosingStrategy
from decider.enemies_detector import EnemiesDetector, DetectionStrategy
from decider.entities_producer import EntitiesProducer
from decider.map_processor import MapProcessor
from decider.units_tracker import UnitsTracker
from decider.house_builder import HouseBuilder
from decider.resource_processor import ResourceProcessor
from decider.utils import find_idle_military_units
from model import *

from decider.units_storage import UnitsStorage


class MyStrategy:
    def __init__(self):
        self.__units_tracker = UnitsTracker()
        self.__builders_hunting_units_director1 = BuilderHuntingUnitsDirector(True)
        self.__builders_hunting_units_director2 = BuilderHuntingUnitsDirector(False)
        self.__house_builder = HouseBuilder()

    def get_action(self, player_view, debug_interface):
        result = Action({})
        my_id = player_view.my_id

        units_storage = UnitsStorage(my_id)
        units_storage.update_storage(player_view.entities)

        military_units_count = len(find_idle_military_units(units_storage.get_allies(), self.__units_tracker))
        enemies_detector = EnemiesDetector(
            DetectionStrategy.BY_BUILDINGS if military_units_count < ZERG_RUSH_READY_AMOUNT else DetectionStrategy.BY_ALL_ENTITES)
        enemies_detector.check_collisions(units_storage.get_allies(), units_storage.get_enemies())

        map_for_tick = MapProcessor(player_view).get_map()

        resource_processor = ResourceProcessor(my_id, player_view.entities)
        current_resource = resource_processor.getMyPlayerResources(player_view)

        entities_producer = EntitiesProducer(DefaultChoosingStrategy(), map_for_tick, self.__house_builder)
        entities_producer.update(result, units_storage, player_view.entity_properties, current_resource)

        self.__house_builder.update(units_storage.get_allies())

        self.make_units_move(enemies_detector, player_view, result, units_storage)
        return result

    def make_units_move(self, enemies_detector, player_view, result, units_storage):

        not_builder_units = units_storage.get_allies()

        # pass if unit build house
        for unit in units_storage.get_allies():
            if self.__house_builder.is_builder(unit.id):
                not_builder_units.remove(unit)

        self.__builders_hunting_units_director1.update(player_view, units_storage.get_enemies(),
                                                       not_builder_units,
                                                       self.__units_tracker, result)
        self.__builders_hunting_units_director2.update(player_view, units_storage.get_enemies(),
                                                       not_builder_units,
                                                       self.__units_tracker, result)
        defensive_battle_units_director = DefensiveBattleUnitsDirector(not_builder_units, self.__units_tracker)
        defensive_battle_units_director.update_commands(enemies_detector.get_collisions(), result)
        builder_units_director = BuilderUnitsDirector(not_builder_units, self.__units_tracker)
        builder_units_director.update_commands(result, player_view.map_size,
                                               player_view.entity_properties[EntityType.BUILDER_UNIT])

        self.__house_builder.update_commands(result)

    def debug_update(self, player_view, debug_interface):
        debug_interface.send(DebugCommand.Clear())
        debug_interface.get_state()
