class FightInfo:
    def __init__(self, fight_length: int, has_world_buffs: bool,
                 has_player_buffs: bool, has_consumables: bool,
                 thick_hide: int):
        self.fight_length = fight_length
        self.armor_multiplier = 4.6 * (1 + thick_hide * 0.02)
        self.has_player_buffs = has_player_buffs
        self.has_world_buffs = has_world_buffs
        self.has_consumables = has_consumables

