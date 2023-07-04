from __future__ import annotations

import copy

import tcod  # type:ignore
import lzma
import pickle
import colour
from engine import Engine
import entity_factories
from game_map import GameWorld

background_image = tcod.image.load("background.png")[:, :, :3]


def new_game(screen_width: int, screen_height: int) -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = screen_width
    map_height = screen_height - 7

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message("The walls shift around you...", colour.welcome_text)

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)
    wooden_bow = copy.deepcopy(entity_factories.wooden_bow)
    small_health_potion = copy.deepcopy(entity_factories.small_health_potion)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory
    wooden_bow.parent = player.inventory
    small_health_potion.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    player.inventory.items.append(wooden_bow)
    player.equipment.toggle_equip(wooden_bow, add_message=False)

    player.inventory.items.append(small_health_potion)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine
