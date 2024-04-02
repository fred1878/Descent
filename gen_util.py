from __future__ import annotations

import random
from typing import List, Tuple, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Item, Entity, Actor
    from procgen import ActorOrItem


def get_items_at_random(
        weighted_chances_by_floor: Dict[int, List[Tuple[Item, int]]],
        number_of_items: int,
        floor: int,
) -> List[Item]:
    item_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                item = value[0]
                weighted_chance = value[1]
                item_weighted_chances[item] = weighted_chance

    items = list(item_weighted_chances.keys())
    item_weighted_chance_values = list(item_weighted_chances.values())

    chosen_items = random.choices(
        items, weights=item_weighted_chance_values, k=number_of_items
    )

    return chosen_items


def get_entities_at_random(
        weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
        number_of_entities: int,
        floor: int,
) -> List[ActorOrItem]:
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


def add_random_items_to_entities(
        equip_chances: Dict[int, List[Tuple[Entity, int]]],
        entity: Actor,
        floor: int):
    for key, values in equip_chances.items():
        if key > floor:
            break
        else:
            for value in values:
                item = value[0]
                weight = value[1]
                if random.randint(0, 99) < weight:
                    entity.inventory.items.append(item)
                    if item.equippable:
                        entity.equipment.toggle_equip(item, entity, add_message=False)
