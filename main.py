from items import *
from fight_info import *


def search_for_best_combo():
    fight_info = FightInfo(fight_length=60, is_fully_buffed=False, thick_hide=2)
    all_items = get_items_dict()
    items_by_slot = get_items_by_slot(all_items)
    item_set_iterator = get_item_iterator(items_by_slot)
    character = Character(fight_info)

    highest_tps = 0
    for i_set, item_set in enumerate(item_set_iterator):
        character.reset_character_gear_and_stats()
        character.add_items_and_validate_set(item_set)
        tps = character.stats.get_tps()
        if tps > highest_tps:
            highest_tps = tps
            print('New record TPS: {:.2f}'.format(tps))
            character.print_equipped_set()
            character.print_stats()


def single_set():
    fight_info = FightInfo(fight_length=60, is_fully_buffed=False, thick_hide=2)
    character = Character(fight_info)
    all_items = get_items_dict()
    character.set_current_items(all_items)
    tps = character.stats.get_tps()
    print('TPS: {:.2f}'.format(tps))
    character.print_equipped_set()
    character.print_stats()

if __name__ == '__main__':
    single_set()
    # search_for_best_combo()
