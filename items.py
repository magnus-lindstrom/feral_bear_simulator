from enum import Enum, auto
from itertools import combinations


class Slots(Enum):
    head = auto()
    neck = auto()
    shoulders = auto()
    back = auto()
    chest = auto()
    wrist = auto()
    hands = auto()
    waist = auto()
    legs = auto()
    feet = auto()
    finger = auto()
    trinket = auto()
    main_hand = auto()
    off_hand = auto()
    two_hand = auto()
    weapon = auto()  # to clump together mh, oh and 2h. Do not assign items to this slot
    # TODO: implement check so that weapon can not be set as an item slot


class Item:
    def __init__(self, name: str, slot: Slots, agility=0,
                 arcane_resistance=0, armor=0, attack_power=0,
                 attack_power_per_two_minutes=0, attack_speed=0,
                 attack_speed_per_two_minutes=0.0, crit=0,
                 defense=0, dodge=0, fire_resistance=0,
                 frost_resistance=0, hit=0, nature_resistance=0,
                 shadow_resistance=0, stamina=0, strength=0, tags=None):
        self.agility = agility
        self.arcane_resistance = arcane_resistance
        self.armor = armor
        self.attack_power = attack_power
        self.attack_power_per_two_minutes = attack_power_per_two_minutes
        self.attack_speed = attack_speed
        self.attack_speed_per_two_minutes = attack_speed_per_two_minutes
        self.crit = crit
        self.defense = defense
        self.dodge = dodge
        self.fire_resistance = fire_resistance
        self.frost_resistance = frost_resistance
        self.hit = hit
        self.name = name
        self.nature_resistance = nature_resistance
        self.shadow_resistance = shadow_resistance
        self.slot = slot
        self.stamina = stamina
        self.strength = strength
        if tags is None:
            self.tags = []
        else:
            self.tags = tags

    def __repr__(self):
        return "<Item: {}>".format(self.name)


class Attributes(Enum):
    agility = auto()
    arcane_resistance = auto()
    armor = auto()
    attack_power = auto()
    attack_power_per_two_minutes = auto()
    attack_speed = auto()
    attack_speed_per_two_minutes = auto()
    crit = auto()
    defense = auto()
    dodge = auto()
    fire_resistance = auto()
    frost_resistance = auto()
    hit = auto()
    name = auto()
    nature_resistance = auto()
    shadow_resistance = auto()
    slot = auto()
    stamina = auto()
    strength = auto()


def validate_items(items):
    invalid_item = False
    slot_list = [s.name for s in Slots]
    attribute_list = [a.name for a in Attributes]
    for item_name, properties in items.items():
        # all properties must be defined and allowed
        for property_name in properties.keys():
            if property_name not in attribute_list:
                print('Item {} has an illegal property: {}'.format(item_name, property_name))
        # the slot attribute must have a valid value
        if properties['slot'] not in slot_list:
            invalid_item = True
            print('Item {} has illegal slot value: {}'.format(item_name, properties['slot']))

    if invalid_item:
        exit(1)


def get_items_by_slot(items: list):
    # returns {slot1: [item1, item2], slot2: [item1, item2]}
    # when slot == ring/trinket/weapon, item is a list of a set of items, such as 2 rings

    new_item_dict = {}
    for item in items:
        if item.slot not in new_item_dict.keys():
            new_item_dict[item.slot] = []
        new_item_dict[item.slot].append(item)

    make_rings_and_trinkets_into_pairs(new_item_dict)
    make_weapons_into_single_slot(new_item_dict)
    return new_item_dict


def make_weapons_into_single_slot(item_dict):
    # make a custom field "weapon" for either two hander or one hander + held in offhand
    item_combos = []
    if 'two_hand' in item_dict.keys():
        # the two handers have to be in a list each, since the other weapons will be
        item_combos.extend([[wep] for wep in item_dict['two_hand']])

    if (Slots.main_hand in item_dict.keys()) and (Slots.off_hand in item_dict.keys()):
        for mh in item_dict[Slots.main_hand]:
            for oh in item_dict[Slots.off_hand]:
                item_combos.append([mh, oh])
    elif Slots.main_hand in item_dict.keys():
        for mh in item_dict[Slots.main_hand]:
            item_combos.append([mh])
    elif Slots.off_hand in item_dict.keys():
        for oh in item_dict[Slots.off_hand]:
            item_combos.append([oh])
    else:
        return  # if no weapons are selected, don't add the extra 'weapon' slot

    # add all weapon combinations to the new weapon slot 'weapon', remove old slots
    item_dict[Slots.weapon] = item_combos
    for key in [Slots.two_hand, Slots.main_hand, Slots.off_hand]:
        if key in item_dict.keys():
            del item_dict[key]


def make_rings_and_trinkets_into_pairs(item_dict):
    for slot in [Slots.finger, Slots.trinket]:
        if slot in item_dict.keys():
            list_of_items = item_dict[slot]
            item_pairs = combinations(list_of_items, 2)
            list_of_item_pairs = [list(item_pair) for item_pair in item_pairs]
            item_dict[slot] = list_of_item_pairs


class Items:
    def get_all_items(self):
        field_names = [attr for attr in dir(self)
                       if not callable(getattr(self, attr))
                       and not attr.startswith("__")]
        return [self.__getattribute__(name) for name in field_names]

    def get_items_from_tag(self, include_tags=None, exclude_tags=None):
        # accepts both a list of tags and individual tags
        if include_tags is None: include_tags = []
        if exclude_tags is None: exclude_tags = []
        if type(include_tags) is not list:
            include_tags = [include_tags]
        if type(exclude_tags) is not list:
            exclude_tags = [exclude_tags]
        items = self.get_all_items()

        # only keep the items that has no exclude tags, unless it also has an include tag
        items = [item for item in items
                 if any(excl_tag in item.tags for excl_tag in exclude_tags)
                 or any(incl_tag in item.tags for incl_tag in include_tags)]
        return items

    # head
    guise_of_the_devourer = Item(
        name="Guise of the devourer",
        slot=Slots.head,
        armor=250,
        strength=17,
        agility=19,
        stamina=36,
        dodge=1,
        tags=['current']
    )
    polar_helmet = Item(
        name="Polar Helmet",
        slot=Slots.head,
        armor=196,
        agility=18,
        stamina=24,
        frost_resistance=44,
        tags=['naxx', 'frost_res']
    )

    # neck
    mark_of_cthun = Item(
        name="Mark of C'thun",
        slot=Slots.neck,
        stamina=24,
        defense=10,
        dodge=1,
        hit=1
    )
    prestors_talisman_of_connivery = Item(
        name="Prestor's Talisman of Connivery",
        slot=Slots.neck,
        agility=30,
        hit=1
    )
    onyxia_tooth_pendant = Item(
        name="Onyxia tooth pendant",
        slot=Slots.neck,
        agility=12,
        stamina=9,
        crit=1,
        hit=1,
        tags=['current']
    )
    sadists_collar = Item(
        name="Sadists Collar",
        slot=Slots.neck,
        stamina=24,
        crit=1,
        attack_power=20,
        tags=['naxx']
    )
    stormrages_talisman_of_seething = Item(
        name="Stormrage's Talisman of Seething",
        slot=Slots.neck,
        stamina=12,
        crit=2,
        attack_power=26,
        tags=['naxx']
    )

    # shoulders
    mantle_of_wicked_revenge = Item(
        name="Mantle of wicked revenge",
        slot=Slots.shoulders,
        armor=170,
        strength=16,
        agility=30,
        stamina=14,
        tags=['current']
    )
    truestrike_shoulders = Item(
        name="Truestrike Shoulders",
        slot=Slots.shoulders,
        armor=129,
        hit=2,
        attack_power=24
    )
    polar_shoulder_pads = Item(
        name="Polar Shoulder Pads",
        slot=Slots.shoulders,
        armor=181,
        stamina=25,
        frost_resistance=33,
        tags=['naxx', 'frost_res']
    )

    # back
    cloak_of_concentrated_hatred = Item(
        name="Cloak of concentrated hatred",
        slot=Slots.back,
        armor=56,
        strength=11,
        agility=16,
        stamina=15,
        hit=1,
        tags=['current']
    )
    cryptfiend_silk_cloak = Item(
        name="Cryptfiend Silk Cloak",
        slot=Slots.back,
        armor=203,
        stamina=14,
        defense=7,
        dodge=1,
        hit=1,
        tags=['naxx']
    )
    cloak_of_the_scourge = Item(
        name="Cloak of the Scourge",
        slot=Slots.back,
        armor=63,
        stamina=23,
        attack_power=30,
        hit=1,
        tags=['naxx']
    )
    shroud_of_dominion = Item(
        name="Shroud of Dominion",
        slot=Slots.back,
        armor=68,
        stamina=11,
        crit=1,
        attack_power=50,
        tags=['naxx']
    )

    # chest
    malfurions_blessed_bulwark = Item(
        name="Malfurions blessed bulwark",
        slot=Slots.chest,
        armor=392,
        strength=40,
        stamina=22,
        tags=['current']
    )
    ghoul_skin_tunic = Item(
        name="Ghoul Skin Tunic",
        slot=Slots.chest,
        armor=411,
        strength=40,
        stamina=22,
        crit=2,
        tags=['current']
    )

    # wrists
    qiraji_execution_bracers = Item(
        name="Qiraji Execution Bracers",
        slot=Slots.wrist,
        armor=103,
        strength=15,
        agility=16,
        stamina=14,
        hit=1,
        tags=['current']
    )

    # hands
    gloves_of_enforcement = Item(
        name="Gloves of enforcement",
        slot=Slots.hands,
        armor=140,
        strength=28,
        agility=20,
        stamina=6,
        hit=1,
        tags=['current']
    )

    # waist
    thick_qirajihide_belt = Item(
        name="Thick qirajihide belt",
        slot=Slots.waist,
        armor=186,
        strength=10,
        agility=17,
        stamina=20,
        tags=['current']
    )
    belt_of_never_ending_agony = Item(
        name="Belt of Never-ending Agony",
        slot=Slots.waist,
        armor=142,
        stamina=20,
        attack_power=64,
        crit=1,
        hit=1,
        tags=['current']
    )

    # legs
    genesis_trousers = Item(
        name="Genesis trousers",
        slot=Slots.legs,
        armor=207,
        strength=12,
        agility=12,
        stamina=22,
        crit=1,
        tags=['current']
    )
    leggings_of_apocalypse = Item(
        name="Leggings of Apocalypse",
        slot=Slots.legs,
        armor=211,
        strength=15,
        agility=31,
        stamina=23,
        crit=2,
        tags=['naxx']
    )

    # feet
    boots_of_the_shadow_flame = Item(
        name="Boots of the shadow flame",
        slot=Slots.feet,
        armor=286,
        stamina=22,
        attack_power=44,
        hit=2,
        tags=['current']
    )
    boots_of_displacement = Item(
        name="Boots of Displacement",
        slot=Slots.feet,
        armor=166,
        agility=33,
        stamina=21,
        tags=['naxx']
    )

    # finger
    band_of_accuria = Item(
        name="Band of Accuria",
        slot=Slots.finger,
        agility=16,
        stamina=10,
        hit=2,
        tags=['current']
    )
    signet_ring_of_the_bronze_dragonflight = Item(
        name="Signet ring of the bronze dragonflight",
        slot=Slots.finger,
        agility=24,
        stamina=13,
        hit=1,
        tags=['current']
    )
    master_dragonslayers_ring = Item(
        name="Master dragonslayers ring",
        slot=Slots.finger,
        stamina=14,
        attack_power=48,
        hit=1
    )
    ring_of_emperor_vek_lor = Item(
        name="Ring of Emperor Vek'lor",
        slot=Slots.finger,
        armor=100,
        agility=12,
        stamina=18,
        defense=9
    )
    heavy_dark_iron_ring = Item(
        name="Heavy Dark Iron Ring",
        slot=Slots.finger,
        armor=110,
        stamina=20,
        defense=5
    )
    circle_of_applied_force = Item(
        name="Circle of Applied Force",
        slot=Slots.finger,
        strength=12,
        agility=22,
        stamina=9
    )
    seal_of_the_gurubashi_berserker = Item(
        name="Seal of the Gurubashi Berserker",
        slot=Slots.finger,
        stamina=13,
        attack_power=40
    )
    hailstone_band = Item(
        name="Hailstone Band",
        slot=Slots.finger,
        stamina=18,
        frost_resistance=20,
        dodge=1,
        tags=['naxx', 'frost_res']
    )
    band_of_unnatural_forces = Item(
        name="Band of Unnatural Forces",
        slot=Slots.finger,
        crit=1,
        hit=1,
        tags=['naxx']
    )
    signed_of_the_fallen_defender = Item(
        name="Signet of the Fallen Defender",
        slot=Slots.finger,
        armor=140,
        stamina=24,
        hit=1,
        tags=['naxx']
    )
    band_of_reanimation = Item(
        name="Band of Reanimation",
        slot=Slots.finger,
        agility=34,
        tags=['naxx']
    )

    # trinket
    earthstrike = Item(
        name="Earthstrike",
        slot=Slots.trinket,
        attack_power_per_two_minutes=47,
        tags=['current']
    )
    drake_fang_talisman = Item(
        name="Drake fang talisman",
        slot=Slots.trinket,
        attack_power=56,
        hit=2,
        dodge=1,
        tags=['current']
    )
    mark_of_tyranny = Item(
        name="Mark of Tyranny",
        slot=Slots.trinket,
        armor=180,
        dodge=1,
        arcane_resistance=10
    )
    heart_of_the_scale = Item(
        name= "Heart of the Scale",
        slot=Slots.trinket,
        fire_resistance=20  # assume fight shorter than 5min
    )
    smoking_heart_of_the_mountain = Item(
        name="Smoking Heart of the Mountain",
        slot=Slots.trinket,
        armor=150,
        arcane_resistance=20,
        fire_resistance=20,
        frost_resistance=20,
        nature_resistance=20,
        shadow_resistance=20
    )
    kiss_of_the_spider = Item(
        name="Kiss of the Spider",
        slot=Slots.trinket,
        crit=1,
        hit=1,
        attack_speed_per_two_minutes=2.5,  # TODO check if this makes sense
        tags=['naxx']
    )
    slayers_crest = Item(
        name="Slayer's Crest",
        slot=Slots.trinket,
        attack_power=64,
        attack_power_per_two_minutes=43,
        tags=['naxx']
    )
    # TODO: add a mode of fighting undead in fight_info, and make atp against undeads
    # mark_of_the_champion = Item(
        # name="Mark of the Champion",
        # slot=Slots.trinket,
        # attack_power=150,
        # tags=['naxx']
    # )

    # two hand
    unyielding_maul = Item(
        name="Blessed qiraji warhammer",
        slot=Slots.two_hand,
        armor=250,
        stamina=12,
        defense=8
    )

    # main hand
    blessed_qiraji_warhammer = Item(
        name="Blessed qiraji warhammer",
        slot=Slots.main_hand,
        armor=70,
        strength=10,
        stamina=12,
        attack_power=280,
        defense=8,
        tags=['current']
    )
    the_end_of_dreams = Item(
        name="The End of Dreams",
        slot=Slots.main_hand,
        stamina=13,
        attack_power=305,
        tags=['naxx']
    )

    # off hand
    tome_of_knowledge = Item(
        name="Tome of knowledge",
        slot=Slots.off_hand,
        strength=8,
        agility=8,
        stamina=8,
        tags=['current']
    )
    magmus_stone = Item(
        name="Magmus Stone",
        slot=Slots.off_hand,
        stamina=7,
        fire_resistance=15
    )