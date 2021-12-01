from decider.battle_units_director import BattleUnitsDirector
from decider.builder_units_director import BuilderUnitsDirector
from decider.default_choosing_strategy import DefaultChoosingStrategy
from decider.enemies_detector import EnemiesDetector
from decider.entities_producer import EntitiesProducer
from decider.map_processor import MapProcessor
from decider.units_tracker import UnitsTracker
from model import *

from decider.units_storage import UnitsStorage


class MyStrategy:
    def __init__(self):
        self.__units_tracker = UnitsTracker()

    def get_action(self, player_view, debug_interface):
        result = Action({})
        my_id = player_view.my_id

        units_storage = UnitsStorage(my_id)
        units_storage.update_storage(player_view.entities)

        enemies_detector = EnemiesDetector()
        enemies_detector.check_collisions(units_storage.get_allies(), units_storage.get_enemies())

        map_for_tick = MapProcessor(player_view).get_map()

        entities_producer = EntitiesProducer(DefaultChoosingStrategy(), map_for_tick)
        entities_producer.update(result, units_storage, player_view.entity_properties)

        battle_units_director = BattleUnitsDirector(units_storage.get_allies(), self.__units_tracker)
        battle_units_director.update_commands(enemies_detector.get_collisions(), result)

        builder_units_director = BuilderUnitsDirector(units_storage.get_allies(), self.__units_tracker)
        builder_units_director.update_commands(result, player_view.map_size,
                                               player_view.entity_properties[EntityType.BUILDER_UNIT])
        return result

    def debug_update(self, player_view, debug_interface):
        debug_interface.send(DebugCommand.Clear())
        debug_interface.get_state()
