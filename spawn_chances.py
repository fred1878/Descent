import entity_factories
from typing import Dict, List, Tuple, TYPE_CHECKING
import tcod  # type: ignore
from engine import Engine
from entity import Entity

max_items_by_floor = [
    (1, 1),
    (4, 2),
    (8, 3)
]

max_monsters_by_floor = [
    (1, 2),
    (2, 3),
    (4, 4),
    (6, 5),
    (8, 6)
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.small_health_potion, 35)],
    1: [(entity_factories.lightning_scroll, 10)],
    2: [(entity_factories.confusion_scroll, 10)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.bronze_sword, 5),
        (entity_factories.health_potion, 10)],
    5: [(entity_factories.wooden_wand, 5)],
    6: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 15), (entity_factories.bronze_sword, 25)],
    7: [(entity_factories.iron_sword, 10), (entity_factories.golden_wand, 5)],
    8: [(entity_factories.fireball_scroll, 35), (entity_factories.plate_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.orc, 30), (entity_factories.hobbit, 30),
        (entity_factories.kobold, 20), (entity_factories.master, 100)],
    2: [(entity_factories.master, 30), (entity_factories.orc, 50)],
    3: [(entity_factories.troll, 15)],
    5: [(entity_factories.orc, 40), (entity_factories.troll, 40)],
    7: [(entity_factories.troll, 60), (entity_factories.reaper, 30)],
}
