from components.ai import *
from components.fighter import Fighter
from entity import Actor, Item
from components.inventory import Inventory
from components import consumable, equippable
from components.level import Level
from components.equipment import Equipment
import colour

player = Actor(
    char="@",
    colour=colour.white,
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=10, base_melee=2, base_magic=1),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=50, current_gold=1000),
)
# fren
shopkeeper = Actor(
    char="S",
    colour=(240, 210, 207),
    name="Shopkeeper",
    ai_cls=ShopAI,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_melee=7, base_magic=0),
    inventory=Inventory(capacity=5),
    level=Level(xp_given=200, gold_given=100),
)
# enemigos
minion = Actor(
    char="m",
    colour=(240, 210, 207),
    name="Minion",
    ai_cls=MinionEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_melee=2, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=15, gold_given=5),
)
master = Actor(
    char="M",
    colour=(240, 210, 207),
    name="Master",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_melee=2, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=15, gold_given=5),
    master=True,
)
kobold = Actor(
    char="k",
    colour=(240, 210, 207),
    name="Kobold",
    ai_cls=HostileRangedEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=3, base_defense=0, base_melee=2, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=15, gold_given=5),
)
hobbit = Actor(
    char="h",
    colour=colour.hobbit,
    name="Hobbit",
    ai_cls=EvasiveEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=6, base_defense=0, base_melee=4, base_ranged=4, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=30, gold_given=5),
)
orc = Actor(
    char="o",
    colour=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_melee=3, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35, gold_given=5),
)
troll = Actor(
    char="T",
    colour=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_melee=5, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100, gold_given=5),
)
reaper = Actor(
    char="R",
    colour=colour.reaper,
    name="Reaper",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=50, base_defense=3, base_melee=9, base_magic=0),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=500, gold_given=5),
)
# items
small_health_potion = Item(
    char="!",
    colour=colour.light_purple,
    name="Small Health Potion",
    consumable=consumable.HealingConsumable(amount=6),
    price=5
)
health_potion = Item(
    char="!",
    colour=colour.light_blue,
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=10),
    price=15
)
lightning_scroll = Item(
    char="~",
    colour=colour.yellow,
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    price=20
)
confusion_scroll = Item(
    char="~",
    colour=colour.purple,
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
    price=15
)
fireball_scroll = Item(
    char="~",
    colour=colour.red,
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
    price=30
)
# equipment
dagger = Item(
    char="/",
    colour=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger(),
    price=20
)

bronze_sword = Item(
    char="/",
    colour=colour.bronze,
    name="Bronze Sword",
    equippable=equippable.BronzeSword(),
    price=60
)

iron_sword = Item(
    char="/",
    colour=colour.iron,
    name="Iron Sword",
    equippable=equippable.IronSword(),
    price=200
)

steel_sword = Item(
    char="/",
    colour=colour.steel,
    name="Steel Sword",
    equippable=equippable.SteelSword(),
    price=500
)

wooden_bow = Item(
    char="D",
    colour=colour.wood,
    name="Wooden Bow",
    equippable=equippable.WoodenBow(),
    price=20
)


wooden_wand = Item(
    char="\\",
    colour=colour.wood,
    name="Wooden Wand",
    equippable=equippable.WoodenWand(),
    price=50
)

golden_wand = Item(
    char="\\",
    colour=colour.gold,
    name="Magic Wand",
    equippable=equippable.GoldenWand(),
    price=250
)

leather_armor = Item(
    char="[",
    colour=colour.leather,
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
    price=20
)

chain_mail = Item(
    char="[",
    colour=colour.steel,
    name="Chain Mail",
    equippable=equippable.ChainMail(),
    price=100
)

plate_mail = Item(
    char="[",
    colour=colour.iron,
    name="Plate Mail",
    equippable=equippable.PlateMail(),
    price=300
)
