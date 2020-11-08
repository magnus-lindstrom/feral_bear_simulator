class FightInfo:
    def __init__(self, fight_length: int, world_buffs: bool, thick_hide: int):
        self.fight_length = fight_length
        self.world_buffs = world_buffs
        self.armor_multiplier = 4.6 * (1 + thick_hide * 0.02)

