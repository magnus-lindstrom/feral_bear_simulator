class FightInfo:
    def __init__(self, fight_length: int, is_fully_buffed: bool, thick_hide: int):
        self.fight_length = fight_length
        self.is_fully_buffed = is_fully_buffed
        self.armor_multiplier = 4.6 * (1 + thick_hide * 0.02)

