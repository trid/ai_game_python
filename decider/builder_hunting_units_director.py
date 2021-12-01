from decider.state_machine.attack_all import AttackAll
from decider.state_machine.move_to import MoveTo
from decider.state_machine.state_machine import StateMachine
from decider.utils import find_idle_military_units, find_units_by_types
from model import EntityType, Vec2Int


class BuilderHuntingUnitsDirector:
    def __init__(self, is_right):
        self.__corner = Vec2Int(0, 0)
        self.__is_right = is_right
        self.__state_machine = StateMachine([])

    def __rebuild_state_machine(self, player_view, enemies, units, units_tracker):
        self.__corner = Vec2Int(0, player_view.map_size - 1) if self.__is_right else Vec2Int(player_view.map_size - 1,
                                                                                             0)
        military_units = find_idle_military_units(units, units_tracker)
        enemy_builders = find_units_by_types(enemies, [EntityType.BUILDER_UNIT])
        if len(military_units) != 0 and len(enemy_builders) != 0:
            target_types = [EntityType.BUILDER_UNIT]
            self.__state_machine = StateMachine([MoveTo(military_units[0], self.__corner),
                                                 AttackAll(military_units[0], enemy_builders[0].position, target_types,
                                                           True)])
            units_tracker.set_unit_working(military_units[0])
        else:
            self.__state_machine = StateMachine([])

    def update(self, player_view, enemies, allies, units_tracker, commands):
        if self.__state_machine.finished():
            self.__rebuild_state_machine(player_view, enemies, allies, units_tracker)
        self.__state_machine.update(player_view, commands)
