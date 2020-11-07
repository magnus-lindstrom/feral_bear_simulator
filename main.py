from items import *
from fight_info import *


if __name__ == '__main__':
    fight_info = FightInfo(fight_length=60, world_buffs=False, thick_hide=5)
    character = Character()
    character.set_current_items()
    character.set_stats(fight_info)
    print('hej')
