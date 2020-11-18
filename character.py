from collections import Counter
import logging

from items import *


class Stats:

    def __init__(self, fight_info):
        self.stat_factor = 1  # without BoK and zg
        self.fight_length = fight_info.fight_length
        self.attack_speed = 2.5
        self.attack_power = 104 + 180 + 90  # base + bear bonus + predatory strikes
        self.attack_speed_tmp_increase = 0
        self.attack_speed_tmp_duration = 0
        self.attack_speed_tmp_cd = 0
        # TODO: move these to after world buffs
        self.crit = 10.15  # sharpened claws, possible base agility
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
        self.enemy_parry_chance = 14  # (%)
        self.enemy_dodge_chance = 6.5  # (%)
        self.chance_to_miss = 9  # (%)

        if fight_info.has_player_buffs:
            # must be run before add_world buffs and before the other player buffs
            self.add_bok()
        if fight_info.has_world_buffs:
            self.add_world_buffs()
        if fight_info.has_player_buffs:
            self.add_all_player_buffs_but_bok()
        if fight_info.has_consumables:
            self.add_food_buffs()

        # player base stats
        self.stamina_addition(69)  # base stamina

    def add_food_buffs(self):
        # mongoose
        self.agility_addition(25)
        self.crit += 2
        # smoked desert dumplings
        self.strength_addition(20)
        # juju might
        self.attack_power += 40
        # juju power
        self.strength_addition(30)
        # R.O.I.D.S
        self.strength_addition(25)
        # gordok green grog
        self.stamina_addition(10)
        # flask of the titans
        self.hit_points += 1200

    def add_bok(self):
        self.stat_factor *= 1.1

    def add_all_player_buffs_but_bok(self):
        # battle shout, increased by talents
        self.attack_power += 232 * 1.25
        # gift of the wild, increased by talents
        self.armor += 285 * 1.35
        self.all_stats_addition(12 * 1.35)
        self.all_resistances_addition(20 * 1.35)
        # leader of the pack
        self.crit += 3
        # trueshot aura
        self.attack_power += 100
        # BoM, increased by talents
        self.attack_power += 185 * 1.2
        # prayer of fortitude, increased by talents
        self.stamina_addition(54 * 1.3)

    def all_resistances_addition(self, increase):
        self.arcane_resistance += increase
        self.fire_resistance += increase
        self.frost_resistance += increase
        self.nature_resistance += increase
        self.shadow_resistance += increase

    def all_stats_addition(self, increase):
        self.strength_addition(increase)
        self.agility_addition(increase)
        self.stamina_addition(increase)

    def add_world_buffs(self):
        # zg
        self.stat_factor *= 1.15
        # ony buff
        self.crit += 5
        self.attack_power += 140
        # dmt
        self.attack_power += 200
        # songflower
        self.crit += 5
        self.agility_addition(15)
        self.strength_addition(15)
        # R.O.I.D.S
        self.strength_addition(25)

    def print_stats(self):
        string = '\n'.join(['Attack speed: {:.2f}'.format(self.attack_speed),
                            'Attack power: {}'.format(self.attack_power),
                            'Crit: {:.2f}'.format(self.crit),
                            'Dodge: {:.2f}'.format(self.dodge),
                            'Armor: {:.0f}'.format(self.armor),
                            'Hit points: {:.0f}'.format(self.hit_points),
                            'Miss chance: {}'.format(self.chance_to_miss)])
        logging.debug('### Current Stats from set ###')
        logging.debug(string)

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

        if item.attack_speed_tmp_increase > 0:
            if self.attack_speed_tmp_increase > 0:
                print('No support for more than one item with attack speed increase.')
                exit(1)
            self.attack_speed_tmp_increase = item.attack_speed_tmp_increase
            self.attack_speed_tmp_duration = item.attack_speed_tmp_duration
            self.attack_speed_tmp_cd = item.attack_speed_tmp_cd

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

    def stamina_addition(self, stamina):
        # 12 atp per strength
        self.hit_points += self.stat_factor * 12 * stamina

    def agility_addition(self, agi):
        self.crit += self.stat_factor * agi / 20
        self.dodge += self.stat_factor * agi / 20
        self.armor += self.stat_factor * agi * 2

    def strength_addition(self, strength):
        # 2 atp per strength
        self.attack_power += self.stat_factor * 2 * strength

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

        if self.attack_speed_tmp_increase > 0:
            if self.fight_length > self.attack_speed_tmp_cd:
                time_without_buff = self.attack_speed_tmp_cd - self.attack_speed_tmp_duration
            else:
                time_without_buff = self.fight_length - self.attack_speed_tmp_duration
            factor = (100 + self.attack_speed_tmp_increase) / 100
            tps *= ((factor * self.attack_speed_tmp_duration
                     + time_without_buff)
                    / self.fight_length)

        return tps


class Character:

    def __init__(self, fight_info):
        self.fight_info = fight_info
        self.stats = Stats(fight_info)
        self.equipped_items = []
        self.stats.add_enchants()

    def print_stats(self):
        self.stats.print_stats()

    def reset_character_gear_and_stats(self):
        self.stats = Stats(self.fight_info)
        self.equipped_items = []
        self.stats.add_enchants()

    def print_equipped_set(self):
        logging.debug('Equipped set:')
        for slot in Slots:
            for item in self.equipped_items:
                if item.slot == slot:
                    logging.debug('{:-<13} {}'.format(slot.name, item.name))

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
