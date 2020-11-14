from statistics import *
from character import *
from fight_info import *
from items import *


def search_for_best_combo():
    fight_info = FightInfo(fight_length=120, is_fully_buffed=False, thick_hide=2)
    items = Items()
    all_items = items.get_items_from_tag(exclude_tags='frost_res')
    items_by_slot = get_items_by_slot(all_items)
    item_set_iterator = get_item_iterator(items_by_slot)
    character = Character(fight_info)

    highest_tps = 0
    for i_set, item_set in enumerate(item_set_iterator):
        if round(i_set/10000) == i_set/10000:
            print("Iteration: {:,}".format(i_set))
        character.reset_character_gear_and_stats()
        character.add_items_and_validate_set(item_set)
        tps = character.stats.get_tps()
        if tps > highest_tps:
            highest_tps = tps
            print('\nSet nr {}. New record TPS: {:.2f}'.format(i_set, tps))
            character.print_equipped_set()
            character.print_stats()


def single_set():
    fight_info = FightInfo(fight_length=120, is_fully_buffed=False, thick_hide=2)
    character = Character(fight_info)
    items = Items()
    item_set = items.get_items_from_tag(include_tags='current')
    character.validate_and_equip_set(item_set)
    tps = character.stats.get_tps()
    print('TPS: {:.2f}'.format(tps))
    character.print_equipped_set()
    character.print_stats()


if __name__ == '__main__':
    # single_set()
    search_for_best_combo()
