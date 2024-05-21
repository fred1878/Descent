from typing import Type, TYPE_CHECKING
import tcod  # type: ignore

from rooms import *
from entity_factories import *
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
    1: [(lightning_scroll, 10), (small_health_potion, 35),
        (cursed_leather_armor, 10), (bronze_mace, 5)],
    2: [(confusion_scroll, 10), (health_potion, 10),
        (bronze_sword, 5), (spiked_leather_armor, 5)],
    3: [(lightning_scroll, 25), (health_potion, 20)],
    4: [(wooden_wand, 5), (bronze_sword, 10)],
    5: [(fireball_scroll, 25), (chain_mail, 15), (iron_sword, 15),
        (bronze_sword, 0)],
    6: [(bloodthirster, 10), (golden_wand, 5),
        (iron_sword, 0), (unstable_pistol, 10)],
    7: [(fireball_scroll, 35), (plate_mail, 15),
        (vampiric_blade, 10)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    1: [(master, 30), (orc, 50),
        (necromancer, 15), (hobbit, 30),
        (kobold, 30), (wizard, 20)],
    2: [(master, 40), (troll, 5)],
    3: [(troll, 15), (skeleton_archer, 15),
        (skeleton, 15), (kobold, 0)],
    4: [(hobbit, 20), (troll, 40),
        (orc, 30), (wizard, 30),
        (necromancer, 30)],
    5: [(orc, 10), (troll, 40)],
    6: [(hobbit, 0), (troll, 70)],
    7: [(troll, 60), (reaper, 30),
        (skeleton, 25), (orc, 0)],
}

item_equip_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(small_health_potion, 50), (leather_armor, 50)],
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
    1: [(small_health_potion, 50), (lightning_scroll, 50)],
    2: [(small_health_potion, 30), (lightning_scroll, 40),
        (confusion_scroll, 30)],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
}