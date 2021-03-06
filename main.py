from statistics import *
from character import *
from configs import *
from items import *
import logging


def search_for_best_combo(fight_info, list_length=100):
    items = Items()
    all_items = items.get_items_from_tag(exclude_tags=['frost_res', 'fire_res', 'def', 'bad'])
    # all_items = items.get_items_from_tag(include_tags='got', exclude_all=True)
    items_by_slot = get_items_by_slot(all_items)
    item_set_iterator = get_item_iterator(items_by_slot)
    secretary = Secretary(list_length)
    character = Character(fight_info)

    print('Total nr of sets: {:,}'.format(get_nr_of_set_combinations(items_by_slot)))
    for i_set, item_set in enumerate(item_set_iterator):
        if round(i_set/10000) == i_set/10000:
            logging.info("Iteration: {:,}".format(i_set))
        character.reset_character_gear_and_stats()
        character.add_items_and_validate_set(item_set)
        tps = character.stats.get_tps()
        secretary.report_tps(tps, i_set, item_set)

    secretary.give_report()


def single_set(fight_info):
    character = Character(fight_info)
    items = Items()
    item_set = items.get_items_from_tag(include_tags='current')
    character.validate_and_equip_set(item_set)
    tps = character.stats.get_tps()
    print('TPS: {:.2f}'.format(tps))
    character.print_equipped_set()
    character.print_stats()


if __name__ == '__main__':
    fi = FightInfo(fight_length=120, has_player_buffs=True, has_consumables=True,
                   has_world_buffs=True, thick_hide=2)
    logging.basicConfig(level=logging.INFO)
    # single_set(fi)
    search_for_best_combo(fi, list_length=10)
