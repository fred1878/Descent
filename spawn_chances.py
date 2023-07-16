from typing import Dict, List, Type
import tcod  # type: ignore

import entity_factories
from rooms import *
from entity import Entity

max_items_by_floor = [
    (1, 1),
    (3, 2),
    (6, 3)
]

max_monsters_by_floor = [
    (1, 2),
    (2, 3),
    (4, 4),
    (6, 5),
    (8, 6)
]

# entity chances override previous floors
item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.small_health_potion, 35), (entity_factories.cursed_leather_armor, 10)],
    1: [(entity_factories.lightning_scroll, 10)],
    2: [(entity_factories.confusion_scroll, 10), (entity_factories.health_potion, 10)],
    3: [(entity_factories.lightning_scroll, 25), (entity_factories.bronze_sword, 5),
        (entity_factories.health_potion, 20)],
    4: [(entity_factories.wooden_wand, 5)],
    5: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 15), (entity_factories.bronze_sword, 25)],
    6: [(entity_factories.iron_sword, 10), (entity_factories.golden_wand, 5)],
    7: [(entity_factories.fireball_scroll, 35), (entity_factories.plate_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.orc, 40), (entity_factories.hobbit, 30),
        (entity_factories.kobold, 30), (entity_factories.master, 20)],
    1: [(entity_factories.master, 30), (entity_factories.orc, 50)],
    2: [(entity_factories.master, 40), (entity_factories.troll, 5)],
    3: [(entity_factories.troll, 15), (entity_factories.skeleton_archer, 15),
        (entity_factories.skeleton, 15), (entity_factories.kobold, 0)],
    4: [(entity_factories.hobbit, 20), (entity_factories.troll, 40),
        (entity_factories.orc, 30)],
    5: [(entity_factories.orc, 10), (entity_factories.troll, 40)],
    6: [(entity_factories.hobbit, 0), (entity_factories.troll, 70)],
    7: [(entity_factories.troll, 60), (entity_factories.reaper, 30)],
}

# room counts are set per floor
room_count: Dict[int, List[Tuple[Type[RectangularRoom], int]]] = {
    1: [(ShopRoom, 1), (TrapRoom, 30)],
    2: [(ShopRoom, 2), (TrapRoom, 5)],
    4: [(ShopRoom, 1), (TrapRoom, 5)],
    5: [(ShopRoom, 1), (TrapRoom, 5)],
    6: [(ShopRoom, 2), (TrapRoom, 5)]
}

shop_params: Dict[int, List[int]] = {
    1: [6, 6],
    2: [8, 8],
    3: [6, 6],
    4: [8, 8],
    5: [6, 6],
    6: [8, 8],
    7: [6, 6],
    8: [8, 8],
}

trap_params: Dict[int, List[int]] = {
    1: [8, 8],
    2: [9, 9],
    3: [9, 9],
    4: [9, 9],
    5: [9, 9],
    6: [9, 9],
    7: [9, 9],
    8: [9, 9],
    9: [9, 9],
    10: [9, 9],
}
