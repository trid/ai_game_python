from decider.battle_units_director import BattleUnitsDirector
from decider.default_choosing_strategy import DefaultChoosingStrategy
from decider.enemies_detector import EnemiesDetector
from decider.entities_producer import EntitiesProducer
from decider.map_processor import MapProcessor
from decider.units_tracker import UnitsTracker
from model import *

from decider.units_storage import UnitsStorage


class MyStrategy:
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

        battle_units_director = BattleUnitsDirector(units_storage.get_allies(), UnitsTracker())
        battle_units_director.update_commands(enemies_detector.get_collisions(), result)

        for entity in player_view.entities:
            if entity.player_id != my_id or entity.entity_type != EntityType.BUILDER_UNIT:
                continue
            properties = player_view.entity_properties[entity.entity_type]

            move_action = None
            build_action = None
            if properties.can_move:
                move_action = MoveAction(
                    Vec2Int(player_view.map_size - 1,
                            player_view.map_size - 1),
                    True,
                    True)
            result.entity_actions[entity.id] = EntityAction(
                move_action,
                build_action,
                AttackAction(None, AutoAttack(properties.sight_range, [
                             EntityType.RESOURCE] if entity.entity_type == EntityType.BUILDER_UNIT else [])),
                None
            )
        return result

    def debug_update(self, player_view, debug_interface):
        debug_interface.send(DebugCommand.Clear())
        debug_interface.get_state()
