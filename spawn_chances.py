from typing import Dict, Type, TYPE_CHECKING, List, Tuple
import tcod  # type: ignore

from rooms import *
import entity_factories
from entity import Entity, Item
if TYPE_CHECKING:
    pass

max_chest_items_by_floor = [
    (1, 2),
    (2, 3),
    (4, 4),
    (6, 5)
]

max_room_items_by_floor = [
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
    1: [(entity_factories.lightning_scroll, 10),(entity_factories.small_health_potion, 35),
        (entity_factories.cursed_leather_armor, 10)],
    2: [(entity_factories.confusion_scroll, 10), (entity_factories.health_potion, 10),
        (entity_factories.bronze_sword, 5)],
    3: [(entity_factories.lightning_scroll, 25), (entity_factories.health_potion, 20)],
    4: [(entity_factories.wooden_wand, 5), (entity_factories.bronze_sword, 10)],
    5: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 15), (entity_factories.iron_sword, 15),
        (entity_factories.bronze_sword, 0)],
    6: [(entity_factories.bloodthirster, 10), (entity_factories.golden_wand, 5),
        (entity_factories.iron_sword, 0)],
    7: [(entity_factories.fireball_scroll, 35), (entity_factories.plate_mail, 15),
        (entity_factories.vampiric_blade, 10)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    1: [(entity_factories.master, 30), (entity_factories.orc, 50),
        (entity_factories.necromancer, 15), (entity_factories.hobbit, 30),
        (entity_factories.kobold, 30), (entity_factories.wizard, 20)],
    2: [(entity_factories.master, 40), (entity_factories.troll, 5)],
    3: [(entity_factories.troll, 15), (entity_factories.skeleton_archer, 15),
        (entity_factories.skeleton, 15), (entity_factories.kobold, 0)],
    4: [(entity_factories.hobbit, 20), (entity_factories.troll, 40),
        (entity_factories.orc, 30), (entity_factories.wizard, 30),
        (entity_factories.necromancer, 30)],
    5: [(entity_factories.orc, 10), (entity_factories.troll, 40)],
    6: [(entity_factories.hobbit, 0), (entity_factories.troll, 70)],
    7: [(entity_factories.troll, 60), (entity_factories.reaper, 30),
        (entity_factories.skeleton, 25), (entity_factories.orc, 0)],
}

item_equip_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.small_health_potion, 50), (entity_factories.leather_armor, 50)],
}

# room counts are set per floor
room_count: Dict[int, List[Tuple[Type[RectangularRoom], int]]] = {
    1: [(ShopRoom, 1), (TrapRoom, 4), (ChestRoom, 15)],
    2: [(ShopRoom, 2), (TrapRoom, 5)],
    3: [(ShopRoom, 2), (TrapRoom, 5)],
    4: [(ShopRoom, 1), (TrapRoom, 6)],
    5: [(ShopRoom, 1), (TrapRoom, 7)],
    6: [(ShopRoom, 2), (TrapRoom, 8)]
}

# params [x, y]
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

# params [x, y]
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

# params [x, y]
chest_room_params: Dict[int, List[int]] = {
    1: [5, 5],
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


chest_item_chances: Dict[int, List[Tuple[Item, int]]] = {
    1: [(entity_factories.small_health_potion, 50), (entity_factories.lightning_scroll, 50)],
    2: [(entity_factories.small_health_potion, 30), (entity_factories.lightning_scroll, 40),
        (entity_factories.confusion_scroll, 30)],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
}