from decider.constants import HOUSE_BUILDERS, BUILDING_HOUSE_SIZE, BUILDING_BASE_SIZE, BUILDING_TURRET_SIZE
from model import BuildAction, MoveAction, RepairAction, Vec2Int, EntityAction, EntityType, Entity
from decider.utils import find_unit_coordinates

from enum import IntEnum


class BuildingState(IntEnum):
    INITIALIZING = 0
    BUILDERS_ARE_GOING = 1
    CREATE_BUILDING = 2
    REPAIR = 3
    ALL_DONE = 4
    FAILED = 5


class BuildingProcess:
    def __init__(self):
        self.builder_id = 0
        self.builder_needed_coord = (0, 0)
        self.coordinates = (0, 0)
        self.reserved_coordinates = []
        self.building_id = 0
        self.building_type = EntityType.HOUSE
        self.state = BuildingState.INITIALIZING
        self.command = EntityAction(None, None, None, None)


class BuildingBuilder:
    def __init__(self, units_tracker):
        self._units_tracker = units_tracker
        self._current_map = {}
        self._buildings_in_progress = []

    @staticmethod
    def get_all_tiles(coord, size):
        building_tiles = []
        for x in range(coord[0], coord[0] + size[0]):
            for y in range(coord[1], coord[1] + size[1]):
                building_tiles.append((x, y))
        return building_tiles

    @staticmethod
    def get_building_size_from_type(building_type):
        print("Entity type: ", building_type)
        if building_type == EntityType.HOUSE:
            return BUILDING_HOUSE_SIZE
        if building_type == EntityType.MELEE_BASE or \
                building_type == EntityType.RANGED_BASE or \
                building_type == EntityType.BUILDER_BASE:
            return BUILDING_BASE_SIZE
        if building_type == EntityType.TURRET:
            return BUILDING_TURRET_SIZE

    def check_if_suitable_position(self, current_map, coord, building_size):
        tiles = BuildingBuilder.get_all_tiles((coord[0] - 1, coord[1] - 1), (building_size[0] + 2, building_size[1] + 2))
        for tile in tiles:
            if current_map.get(tile) is not None:
                return False
            for building_process in self._buildings_in_progress:
                if tile in building_process.reserved_coordinates:
                    return False

        return True

    def buildings_in_progress_count(self, building_type):
        return len(self._buildings_in_progress)

    def get_builder(self, house_coord, units):
        # Need to sort by distance
        builders = list(filter(lambda item: item.entity_type == EntityType.BUILDER_UNIT, units))
        if len(builders) == 0:
            return None
        # Get first unoccupied
        for builder in builders:
            if self._units_tracker.is_unit_idle(builder):
                self._units_tracker.set_unit_working(builder)
                return builder

    def find_suitable_coordinates(self, current_map, building_size):
        map_size = 50
        distance_from_the_corner = 0

        while distance_from_the_corner < map_size:
            for x in range(distance_from_the_corner):
                y = distance_from_the_corner - x
                if self.check_if_suitable_position(current_map, (x, y), building_size):
                    print("NEW BUILDING SUITABLE: ", (x, y))
                    return x, y

            distance_from_the_corner += 1

    def request_building(self, commands_list, current_map, units, building_type):
        print("Building requested")
        ######
        # if self.buildings_in_progress_count(building_type) > 2:
        #     return
        ######
        building_process = BuildingProcess()
        building_process.state = BuildingState.INITIALIZING

        building_process.building_type = building_type

        building_size = self.get_building_size_from_type(building_type)

        coordinates = self.find_suitable_coordinates(current_map, building_size)
        building_process.coordinates = coordinates

        # TODO: One builder for now. Should be multiple
        builder = self.get_builder(coordinates, units)
        if builder is None:
            return

        building_process.reserved_coordinates = self.get_all_tiles(coordinates, building_size)

        building_process.builder = builder

        building_process.builder_needed_coord = (coordinates[0] + building_size[0], coordinates[1] + building_size[1] - 1)

        self._buildings_in_progress.append(building_process)

    def update(self, current_map):
        for building_process in self._buildings_in_progress:
            move_action = None
            build_action = None
            repair_action = None

            if building_process.state == BuildingState.INITIALIZING:
                move_action = MoveAction(
                    Vec2Int(building_process.builder_needed_coord[0], building_process.builder_needed_coord[1]),
                    False,
                    False)

                building_process.state = BuildingState.BUILDERS_ARE_GOING
                print("Builder id:", building_process.builder.id, "New state: ", building_process.state)

            if building_process.state == BuildingState.BUILDERS_ARE_GOING:
                if find_unit_coordinates(building_process.builder.id, current_map) == building_process.builder_needed_coord:
                    build_action = BuildAction(EntityType.HOUSE,
                                               Vec2Int(building_process.coordinates[0],
                                                       building_process.coordinates[1]))
                    building_process.state = BuildingState.CREATE_BUILDING
                    print("Builder id:", building_process.builder.id, "New state: ", building_process.state)

            elif building_process.state == BuildingState.CREATE_BUILDING or building_process.state == BuildingState.REPAIR:
                building = current_map.get(building_process.coordinates)
                # TODO: health shouldn't be 50
                if not building:
                    print("Something is wrong! Abort building")
                    building_process.state = BuildingState.FAILED
                    print("Builder id:", building_process.builder.id, "New state: ", building_process.state)
                    continue

                if building.health < 50:
                    if building_process.state != BuildingState.REPAIR:
                        building_process.state = BuildingState.REPAIR
                        print("Builder id:", building_process.builder.id, "New state: ", building_process.state)
                    repair_action = RepairAction(building.id)
                else:
                    building_process.state = BuildingState.ALL_DONE
                    print("Builder id:", building_process.builder.id, "New state: ", building_process.state)

            if move_action or build_action or repair_action:
                building_process.command = EntityAction(move_action, build_action, None, repair_action)
                print("Builder id:", building_process.builder.id, "Entity action: ", building_process.command)

            if building_process.state == BuildingState.ALL_DONE or building_process.state == BuildingState.FAILED:
                self._units_tracker.set_unit_idle(building_process.builder)
                self._buildings_in_progress.remove(building_process)

    def update_commands(self, commands):
        for building_process in self._buildings_in_progress:
            if building_process.command:
                commands.entity_actions[building_process.builder.id] = building_process.command
                building_process.command = None
