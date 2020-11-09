from items import *
from fight_info import *


def search_for_best_combo():
    fight_info = FightInfo(fight_length=60, world_buffs=False, thick_hide=2)
    character = Character()
    character.iterate_over_combinations()


def single_set():
    fight_info = FightInfo(fight_length=60, world_buffs=False, thick_hide=2)
    character = Character()
    character.set_current_items()
    character.set_stats(fight_info)


if __name__ == '__main__':
    single_set()
    print('hej')
