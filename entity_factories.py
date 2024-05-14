from components.ability import Ability
from components.ai import *
from components.fighter import Fighter
from components.attribute import Attribute
from entity import Actor, Item, Chest
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
    fighter=Fighter(hp=30, base_defense=0, base_melee=2, base_magic=0),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=50, current_gold=0),
    attribute=Attribute(),
    friendly=True,
    ability=Ability()
)
# fren
shopkeeper = Actor(
    char="S",
    colour=(240, 210, 207),
    name="Shopkeeper",
    ai_cls=ShopAI,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=2, base_melee=7),
    inventory=Inventory(capacity=20),
    level=Level(xp_given=200, gold_given=1000),
    attribute=Attribute(),
    friendly=True,
    ability=Ability()
)
ally = Actor(
    char="A",
    colour=(240, 210, 207),
    name="Ally",
    ai_cls=AllyAI,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=2, base_melee=7),
    inventory=Inventory(capacity=20),
    level=Level(xp_given=200, gold_given=1000),
    attribute=Attribute(),
    friendly=True,
    ability=Ability()
)
tentacle_ally = Actor(
    char="T",
    colour=colour.black,
    name="Tentacle",
    ai_cls=StationaryAllyAI,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0,  base_range=2, base_ranged=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0, gold_given=0),
    attribute=Attribute(),
    friendly=True,
    ability=Ability()
)
# enemigos
minion = Actor(
    char="m",
    colour=(240, 210, 207),
    name="Minion",
    ai_cls=MinionEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=5, base_defense=0, base_melee=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=15, gold_given=0),
    attribute=Attribute(),
    ability=Ability()
)
master = Actor(
    char="M",
    colour=(240, 210, 207),
    name="Master",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_melee=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=50, gold_given=30),
    master=True,
    attribute=Attribute(),
    ability=Ability()
)
kobold = Actor(
    char="k",
    colour=(240, 210, 207),
    name="Kobold",
    ai_cls=HostileRangedEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=8, base_defense=0, base_ranged=2, base_range=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=30, gold_given=5),
    attribute=Attribute(),
    ability=Ability()
)
skeleton = Actor(
    char="s",
    colour=colour.white,
    name="Skeleton",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=15, base_defense=0, base_melee=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=80, gold_given=20),
    attribute=Attribute(),
    ability=Ability()
)
skeleton_archer = Actor(
    char="s",
    colour=colour.white,
    name="Skeleton Archer",
    ai_cls=HostileRangedEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=12, base_defense=0, base_ranged=3, base_range=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=80, gold_given=20),
    attribute=Attribute(),
    ability=Ability()
)
hobbit = Actor(
    char="h",
    colour=colour.hobbit,
    name="Hobbit",
    ai_cls=EvasiveEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=6, base_defense=0, base_melee=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=30, gold_given=5),
    attribute=Attribute(),
    ability=Ability()
)
wizard = Actor(
    char="w",
    colour=colour.white,
    name="Wizard",
    ai_cls=HostileAttackDebufferEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_melee=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=50, gold_given=10),
    attribute=Attribute(),
    ability=Ability()
)
necromancer = Actor(
    char="n",
    colour=colour.reaper,
    name="Necromancer",
    ai_cls=NecromancerEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_melee=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100, gold_given=10),
    attribute=Attribute(),
    ability=Ability()
)
orc = Actor(
    char="o",
    colour=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_melee=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35, gold_given=5),
    attribute=Attribute(),
    ability=Ability()
)
troll = Actor(
    char="T",
    colour=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_melee=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100, gold_given=25),
    attribute=Attribute(),
    ability=Ability()
)
reaper = Actor(
    char="R",
    colour=colour.reaper,
    name="Reaper",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=50, base_defense=3, base_melee=9),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=500, gold_given=300),
    attribute=Attribute(),
    ability=Ability()
)
# dungeon objects
chest = Chest(
    colour=colour.sandy_brown,
    opened_colour=colour.saddle_brown,
    inventory=Inventory(capacity=5)
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
resurrect_scroll = Item(
    char="~",
    colour=colour.black,
    name="Resurrect Scroll",
    consumable=consumable.ResurrectConsumable(),
    price=30
)
attack_debuff_scroll = Item(
    char="~",
    colour=colour.dark_red,
    name="Attack Debuff Scroll",
    consumable=consumable.AttackDebuffConsumable(radius=3.5),
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

dark_sword = Item(
    char="/",
    colour=colour.black,
    name="Dark Sword",
    equippable=equippable.DarkSword(),
    price=1000
)

vampiric_blade = Item(
    char="/",
    colour=colour.blood,
    name="Vampiric Blade",
    equippable=equippable.VampiricBlade(),
    price=1000
)

bloodthirster = Item(
    char="/",
    colour=colour.red,
    name="Bloodthirster",
    equippable=equippable.Bloodthirster(),
    price=800
)

wooden_bow = Item(
    char="D",
    colour=colour.wood,
    name="Wooden Bow",
    equippable=equippable.WoodenBow(),
    price=20
)

composite_wooden_bow = Item(
    char="D",
    colour=colour.light_wood,
    name="Composite Wooden Bow",
    equippable=equippable.CompositeWoodenBow(),
    price=120
)

unstable_pistol = Item(
    char="P",
    colour=colour.light_blue,
    name="Unstable Pistol",
    equippable=equippable.UnstablePistol(),
    price=200
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

cursed_orb = Item(
    char="\\",
    colour=colour.black,
    name="Cursed Orb",
    equippable=equippable.CursedOrb(),
    price=450
)
# Armor
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

cursed_leather_armor = Item(
    char="[",
    colour=colour.black,
    name="Cursed Leather Armor",
    equippable=equippable.CursedLeatherArmor(),
    price=20
)
