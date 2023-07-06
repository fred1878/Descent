from __future__ import annotations
import random
from itertools import repeat
from typing import Dict, Iterator, List, Type
import tcod  # type: ignore

from exceptions import RoomNotFound
from rooms import *
from spawn_chances import max_items_by_floor, max_monsters_by_floor, item_chances, enemy_chances, room_count, \
    shop_params
from engine import Engine
from entity import Entity, Actor
import tile_types


def get_max_value_for_floor(max_value_by_floor: List[Tuple[int, int]], floor: int) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value


def get_entities_at_random(
        weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
        number_of_entities: int,
        floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]
                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities


def place_entities(room: RectangularRoom, dungeon: game_map.GameMap, floor_number: int) -> None:
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, floor_number)
    )

    monsters: List[Entity] = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        item_chances, number_of_items, floor_number
    )

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)

            if isinstance(entity, Actor):
                if entity.master:
                    minion_spawn_locations = (
                        [
                            (x + 1, y + 1),
                            (x + 1, y),
                            (x + 1, y - 1),
                            (x, y + 1),
                            (x, y - 1),
                            (x - 1, y + 1),
                            (x - 1, y),
                            (x - 1, y - 1),
                        ]
                    )
                    valid_locations = list(filter(lambda s: valid_spawn(room, s), minion_spawn_locations))

                    spawn_x, spawn_y = random.choice(valid_locations)
                    entity_factories.minion.spawn(dungeon, spawn_x, spawn_y)


def valid_spawn(room: RectangularRoom, xy: Tuple[int, int]) -> bool:
    x, y = xy
    return room.inner[0].start < x < room.inner[0].stop and room.inner[1].start < y < room.inner[1].stop


def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if bool(random.getrandbits(1)):  # 50% chance.
        corner_x, corner_y = x2, y1  # Move horizontally, then vertically.
    else:
        corner_x, corner_y = x1, y2  # Move vertically, then horizontally.

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def intersects(self, other: RectangularRoom) -> bool:
    """Return True if this room overlaps with another RectangularRoom."""
    return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1)

    return dungeon


def get_custom_rooms(
        number_of_rooms_by_floor: Dict[int, List[Tuple[Type[RectangularRoom], int]]],
        floor: int
) -> List[Type[RectangularRoom]]:
    rooms: List[Type[RectangularRoom]] = []
    for key, values in number_of_rooms_by_floor.items():
        if key == floor:
            for value in values:
                room, number_of_room = value
                rooms.extend(repeat(room, number_of_room))

    return rooms


def generate_custom_rooms(
        dungeon: game_map.GameMap,
        floor: int) -> List[RectangularRoom]:
    rooms: List[RectangularRoom] = []
    room_types: List[Type[RectangularRoom]] = get_custom_rooms(room_count, floor)
    for room in room_types:
        if room.__name__ == 'ShopRoom':
            for key, values in shop_params.items():
                if key == floor:
                    room_width = values[0]
                    room_height = values[1]
                    x = random.randint(0, dungeon.width - room_width - 1)
                    y = random.randint(0, dungeon.height - room_height - 1)
                    new_room = room(x, y, room_width, room_height, dungeon)
                    dungeon.tiles[new_room.inner] = tile_types.floor
                    rooms.append(new_room)
        else:
            raise RoomNotFound(str(room.__name__) + " not in room generator")
    return rooms


def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        engine: Engine,
) -> game_map.GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = game_map.GameMap(engine, map_width, map_height, entities=[player])
    current_floor = engine.game_world.current_floor

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    custom_rooms = generate_custom_rooms(dungeon, current_floor)
    rooms.extend(custom_rooms)

    number_of_custom_rooms = len(rooms)

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out current rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) != 0:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
            center_of_last_room = new_room.center

        if len(rooms) == number_of_custom_rooms:
            # The first room, where the player starts.
            player.place(*new_room.center, dungeon)

        place_entities(new_room, dungeon, current_floor)
        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room
        # Finally, append the new room to the list.
        rooms.append(new_room)

    entity_factories.dark_sword.spawn(dungeon, player.x, player.y + 1)

    for entity in dungeon.entities:
        print(entity.name + " " + str(entity.x) + " " + str(entity.y))
    print("stairs x:" + str(dungeon.downstairs_location[0]), "y: " + str(dungeon.downstairs_location[1]))

    return dungeon
