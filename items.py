from enum import Enum, auto
from collections import Counter
import yaml

from statistics import *


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
    agility = auto()
    armor = auto()
    attack_power = auto()
    attack_power_per_two_minutes = auto()
    attack_speed = auto()
    crit = auto()
    defense = auto()
    dodge = auto()
    hit = auto()
    name = auto()
    slot = auto()
    stamina = auto()
    strength = auto()


def get_items_dict():
    with open("items.yaml") as f:
        all_items = yaml.load(f, Loader=yaml.FullLoader)
    all_items = add_default_values_and_check_names(all_items)
    validate_items(all_items)
    return all_items


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


def add_default_values_and_check_names(items):
    attribute_list = [a.name for a in Attributes]
    for name, item in items.items():
        if 'name' not in item.keys():
            print('item missing name element: {}'.format(name))
            exit(1)
        for attribute in attribute_list:
            if attribute not in item.keys():
                item[attribute] = 0

    return items


def print_set_info(items: list, set_number: int):
    list_of_names = [item['name'] for item in items]
    string = '\n'.join(list_of_names)
    print('set {}:'.format(set_number))
    print(string)


def get_items_by_slot(items):
    # returns {slot1: [item1, item1], slot2: [item2, item2]}
    new_item_dict = {}
    for _, item in items.items():
        if item['slot'] not in new_item_dict.keys():
            new_item_dict[item['slot']] = []
        new_item_dict[item['slot']].append(item)
    return new_item_dict


class Stats:

    def __init__(self, fully_buffed: bool):
        if fully_buffed:
            print('no support yet for world buffs')
            exit(1)
        self.attack_speed = 2.5
        self.attack_power = 0
        self.crit = 13.15  # leader of the pack, sharpened claws, possible base agility
        self.dodge = 5.15
        self.armor = 130
        self.defense = 300
        self.hit_points = 1483  # base hp
        self.hit_points += 1240  # from dire bear form
        self.hit_points -= 180  # needed to make things add up
        self.hit_points += 69 * 10 * 1.2  # base stamina

        self.enemy_parry_chance = 14  # (%)
        self.enemy_dodge_chance = 6.5  # (%)
        self.chance_to_miss = 8  # (%)

    def add_to_stats(self, item, fight_info):

        self.attack_power += item['attack_power']
        self.attack_power += 2 * item['strength']
        if fight_info.fight_length < 120:
            self.attack_power += item['attack_power_per_two_minutes'] \
                                 / fight_info.fight_length * 120
        else:
            # assume inf fight length if longer than 2min
            self.attack_power += item['attack_power_per_two_minutes']
        self.crit += item['crit']
        if self.chance_to_miss == 8:
            # first hit is removed
            self.chance_to_miss -= max(item['hit'] - 1, 0)
        else:
            self.chance_to_miss = max(self.chance_to_miss - item['hit'], 0)
        self.dodge += item['dodge']
        self.dodge += item['defense'] * 0.04
        self.armor += item['armor'] * fight_info.armor_multiplier
        self.agility_addition(item['agility'])
        self.hit_points += item['stamina'] * 10 * 1.2  # heart of the wild

        assert item['attack_speed'] == 0, 'no support for item attack speed yet'

    def add_enchants(self):
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

    def get_tps(self):
        base_attack_dmg = 126.5
        avg_melee_hit = base_attack_dmg \
                        + self.attack_power * 2.5 / 14
        avg_maul = avg_melee_hit + 128
        avg_maul_with_misses = avg_maul * \
                               (100 - self.enemy_parry_chance
                                    - self.enemy_dodge_chance
                                    - self.chance_to_miss) / 100
        avg_maul_incl_crit = avg_maul_with_misses * (1 + self.crit/100)
        dps = avg_maul_incl_crit / self.attack_speed
        tps = dps * 1.45 * 1.7  # assuming 5/5 feral instinct
        return tps


class Character:

    def __init__(self, fight_info):
        self.fight_info = fight_info
        self.stats = Stats(fight_info.is_fully_buffed)
        self.equipped_items = []
        self.stats.add_enchants()

    def reset_character_gear_and_stats(self):
        self.stats = Stats(self.fight_info.is_fully_buffed)
        self.equipped_items = []
        self.stats.add_enchants()

    def add_items_and_validate_set(self, items):
        if type(items) is not list:
            items = [items]
        for item in items:
            self.equipped_items.append(item)
            self.stats.add_to_stats(item, self.fight_info)
        self.validate_item_composition()

    def set_current_items(self, all_items):
        self.reset_character_gear_and_stats()
        self.add_items_and_validate_set(
            [all_items[item_name] for item_name in current_set_names]
        )

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


current_set_names = [
    'guise_of_the_devourer',
    'onyxia_tooth_pendant',
    'mantle_of_wicked_revenge',
    'cloak_of_concentrated_hatred',
    'malfurions_blessed_bulwark',
    'wristguards_of_stability',
    'gloves_of_enforcement',
    'thick_qirajihide_belt',
    'genesis_trousers'
    'boots_of_the_shadow_flame',
    'signet_ring_of_the_bronze_dragonflight',
    'master_dragonslayers_ring',
    'earthstrike',
    'drake_fang_talisman',
    'blessed_qiraji_warhammer',
    'tome_of_knowledge'
    ]
