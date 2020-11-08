from enum import Enum, auto
from collections import Counter
import yaml


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


class Attributes(Enum):
    armor = auto()
    dodge = auto()
    defense = auto()
    strength = auto()
    stamina = auto()
    agility = auto()
    hit = auto()
    crit = auto()
    attack_speed = auto()
    slot = auto()
    attack_power = auto()
    attack_power_per_two_minutes = auto()


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


def add_default_values(items):
    attribute_list = [a.name for a in Attributes]
    for name, item in items.items():
        for attribute in attribute_list:
            if attribute not in item.keys():
                item[attribute] = 0

    return items


class Wardrobe:
    with open("items.yaml") as f:
        all_items = yaml.load(f, Loader=yaml.FullLoader)
    all_items = add_default_values(all_items)
    validate_items(all_items)
    equipped_items = []

    def set_current_items(self):
        self.equipped_items = []
        self.equipped_items.append(self.all_items['guise_of_the_devourer'])
        self.equipped_items.append(self.all_items['onyxia_tooth_pendant'])
        self.equipped_items.append(self.all_items['mantle_of_wicked_revenge'])
        self.equipped_items.append(self.all_items['cloak_of_concentrated_hatred'])
        self.equipped_items.append(self.all_items['malfurions_blessed_bulwark'])
        self.equipped_items.append(self.all_items['wristguards_of_stability'])
        self.equipped_items.append(self.all_items['gloves_of_enforcement'])
        self.equipped_items.append(self.all_items['thick_qirajihide_belt'])
        self.equipped_items.append(self.all_items['genesis_trousers'])
        self.equipped_items.append(self.all_items['boots_of_the_shadow_flame'])
        self.equipped_items.append(self.all_items['signet_ring_of_the_bronze_dragonflight'])
        self.equipped_items.append(self.all_items['master_dragonslayers_ring'])
        self.equipped_items.append(self.all_items['earthstrike'])
        self.equipped_items.append(self.all_items['drake_fang_talisman'])
        self.equipped_items.append(self.all_items['blessed_qiraji_warhammer'])
        self.equipped_items.append(self.all_items['tome_of_knowledge'])

    def validate_item_composition(self):
        used_slots = [item['slot'] for item in self.equipped_items]
        slot_counter = Counter(used_slots)
        for slot_name in [s.name for s in Slots]:
            if slot_name in ['finger', 'trinket']:
                assert slot_counter[slot_name] <= 2
            else:
                assert slot_counter[slot_name] <= 1

        if slot_counter['two_hand'] == 1:
            assert slot_counter['main_hand'] == 0
            assert slot_counter['off_hand'] == 0
        if slot_counter['main_hand'] == 1:
            assert slot_counter['two_hand'] == 0


class Stats:
    attack_speed = 0
    attack_power = 0
    crit = 13.15  # leader of the pack, sharpened claws, possible base agility
    hit = 0
    dodge = 5.15
    armor = 130
    defense = 300
    hit_points = 1483  # base hp
    hit_points += 1240  # from dire bear form
    hit_points -= 180  # needed to make things add up
    hit_points += 69 * 10 * 1.2  # base stamina

    def add_to_stats(self, items, fight_info):
        if fight_info.world_buffs:
            print('no support yet for world buffs')
            exit(1)

        for item in items:
            self.attack_power += item['attack_power']
            self.attack_power += 2 * item['strength']
            if fight_info.fight_length < 120:
                self.attack_power += item['attack_power_per_two_minutes'] \
                                     / fight_info.fight_length * 120
            else:
                # assume inf fight length if longer than 2min
                self.attack_power += item['attack_power_per_two_minutes']
            self.crit += item['crit']
            self.hit += item['hit']
            self.dodge += item['dodge']
            self.dodge += item['defense'] * 0.04
            self.armor += item['armor'] * fight_info.armor_multiplier
            self.agility_addition(item['agility'])
            self.hit_points += item['stamina'] * 10 * 1.2  # heart of the wild

            assert item['attack_speed'] == 0, 'no support for item attack speed yet'

    def add_enchants(self, fight_info):
        # head enchant
        self.attack_speed /= 1.01
        # shoulder enchant
        self.attack_power += 30
        # back
        self.agility_addition(3)
        # chest, agility
        self.agility_addition(4)
        # chest, strength
        self.attack_power += 2 * 4
        # chest, stamina
        self.hit_points += 4 * 10 * 1.2
        # wrists
        self.attack_power = 2 * 9
        # hands
        self.agility_addition(15)
        # legs
        self.attack_speed /= 1.01
        # feet
        self.agility_addition(7)
        # weapon
        self.attack_power += 2 * 15

    def agility_addition(self, agi):
        self.crit += agi / 20
        self.dodge += agi / 20
        self.armor += agi * 2


class Character:
    wardrobe = Wardrobe()
    stats = Stats()

    def set_current_items(self):
        self.wardrobe.set_current_items()
        self.wardrobe.validate_item_composition()

    def set_stats(self, fight_info):
        self.stats.add_to_stats(self.wardrobe.equipped_items, fight_info)
        self.stats.add_enchants(fight_info)
