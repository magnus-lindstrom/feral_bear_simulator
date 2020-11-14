from collections import Counter

from items import *


class Stats:

    def __init__(self, fully_buffed: bool):
        if fully_buffed:
            print('no support yet for world buffs')
            exit(1)
        self.attack_speed = 2.5
        self.attack_power = 104 + 180 + 90  # base + bear bonus + predatory strikes
        self.crit = 13.15  # leader of the pack, sharpened claws, possible base agility
        self.dodge = 5.15  # night elf
        self.armor = 130
        self.arcane_resistance = 0
        self.fire_resistance = 0
        self.frost_resistance = 0
        self.nature_resistance = 10  # night elf
        self.shadow_resistance = 0
        self.hit_points = 1483  # base hp
        self.hit_points += 1240  # from dire bear form
        self.hit_points -= 180  # needed to make things add up
        self.hit_points += 69 * 10 * 1.2  # base stamina

        self.enemy_parry_chance = 14  # (%)
        self.enemy_dodge_chance = 6.5  # (%)
        self.chance_to_miss = 9  # (%)

    def print_stats(self):
        string = '\n'.join(['Attack speed: {:.2f}'.format(self.attack_speed),
                            'Attack power: {}'.format(self.attack_power),
                            'Crit: {:.2f}'.format(self.crit),
                            'Dodge: {:.2f}'.format(self.dodge),
                            'Armor: {:.0f}'.format(self.armor),
                            'Hit points: {:.0f}'.format(self.hit_points),
                            'Miss chance: {}'.format(self.chance_to_miss)])
        print('### Current Stats from set ###')
        print(string)

    def add_to_stats(self, item: Item, fight_info):

        # defensive
        self.hit_points += item.stamina * 10 * 1.2  # heart of the wild
        self.dodge += item.dodge
        self.dodge += item.defense * 0.04
        self.armor += item.armor * fight_info.armor_multiplier
        self.arcane_resistance += item.arcane_resistance
        self.fire_resistance += item.fire_resistance
        self.frost_resistance += item.frost_resistance
        self.nature_resistance += item.nature_resistance
        self.shadow_resistance += item.shadow_resistance

        # offensive
        self.attack_power += item.attack_power
        self.crit += item.crit
        self.chance_to_miss = max(self.chance_to_miss - item.hit, 0)
        self.agility_addition(item.agility)
        self.strength_addition(item.strength)
        if fight_info.fight_length < 120:
            self.attack_power += item.attack_power_per_two_minutes \
                                 / fight_info.fight_length * 120
        else:
            # assume inf fight length if longer than 2min
            self.attack_power += item.attack_power_per_two_minutes

        assert item.attack_speed == 0, 'no support for item attack speed yet'

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
        self.strength_addition(4)
        # chest, stamina
        self.hit_points += 4 * 10 * 1.2
        # wrists
        self.strength_addition(9)
        # hands
        self.agility_addition(15)
        # legs
        self.attack_speed /= 1.01
        # feet
        self.agility_addition(7)
        # weapon
        self.strength_addition(15)

    def agility_addition(self, agi):
        self.crit += agi / 20
        self.dodge += agi / 20
        self.armor += agi * 2

    def strength_addition(self, strength):
        # 2 atp per strength
        self.attack_power += 2 * strength

    def get_tps(self):
        if self.chance_to_miss == 9:
            self.chance_to_miss = 8

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

    def print_stats(self):
        self.stats.print_stats()

    def reset_character_gear_and_stats(self):
        self.stats = Stats(self.fight_info.is_fully_buffed)
        self.equipped_items = []
        self.stats.add_enchants()

    def print_equipped_set(self):
        print('Equipped set:')
        for slot in Slots:
            for item in self.equipped_items:
                if item.slot == slot:
                    print('{:-<13} {}'.format(slot.name, item.name))

    def add_items_and_validate_set(self, items):
        if type(items) is not list:
            items = [items]
        for item in items:
            self.equipped_items.append(item)
            self.stats.add_to_stats(item, self.fight_info)
        self.validate_item_composition()

    def validate_and_equip_set(self, item_set):
        self.reset_character_gear_and_stats()
        self.add_items_and_validate_set(
            [item for item in item_set]
        )

    def validate_item_composition(self):
        used_slots = [item.slot for item in self.equipped_items]
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
    'qiraji_execution_bracers',
    'gloves_of_enforcement',
    'thick_qirajihide_belt',
    'genesis_trousers',
    'boots_of_the_shadow_flame',
    'signet_ring_of_the_bronze_dragonflight',
    'master_dragonslayers_ring',
    'earthstrike',
    'drake_fang_talisman',
    'blessed_qiraji_warhammer',
    'tome_of_knowledge'
    ]
