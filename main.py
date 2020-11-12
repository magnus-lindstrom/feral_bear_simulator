from items import *
from fight_info import *


def search_for_best_combo():
    fight_info = FightInfo(fight_length=60, is_fully_buffed=False, thick_hide=2)
    all_items = get_items_dict()
    items_by_slot = get_items_by_slot(all_items)
    item_set_iterator = get_item_iterator(items_by_slot)
    character = Character(fight_info)

    tps_vector = []
    for i_set, item_set in enumerate(item_set_iterator):
        print_set_info(item_set, i_set)
        character.reset_character_gear_and_stats()
        character.add_items_and_validate_set(item_set)
        tps = character.stats.get_tps()
        tps_vector.append(tps)
        print('Threat per second: {:.2f}'.format(tps))



def single_set():
    fight_info = FightInfo(fight_length=60, is_fully_buffed=False, thick_hide=2)
    character = Character()
    character.set_current_items()
    character.set_stats(fight_info)


if __name__ == '__main__':
    # single_set()
    search_for_best_combo()
