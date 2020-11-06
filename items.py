from enum import Enum, auto
import yaml


class Slots(Enum):
    head = auto()
    neck = auto()
    shoulders = auto()
    back = auto()
    chest = auto()
    wrist = auto()
    hands = auto()
    waist = auto()
    legs = auto()
    feet = auto()
    ring = auto()
    trinket = auto()
    main_hand = auto()
    off_hand = auto()
    two_hand = auto()


class Attributes(Enum):
    armor = auto()
    strength = auto()
    stamina = auto()
    agility = auto()
    hit = auto()
    crit = auto()
    slot = auto()
    attack_power = auto()


class Wardrobe:
    items = None

    def set_current_items(self):
        # Just loads the entire character atm
        with open("items.yaml") as f:
            self.items = yaml.load(f, Loader=yaml.FullLoader)

    def validate_items(self):
        invalid_item = False
        slot_list = [s.name for s in Slots]
        attribute_list = [a.name for a in Attributes]
        for item_name, properties in self.items.items():
            # all properties must be defined and allowed
            for property_name in properties.keys():
                if property_name not in attribute_list:
                    print('Item {} has an illegal property: {}'.format(item_name, property_name))
            # the slot attribute must have a valid value
            if properties['slot'] not in slot_list:
                invalid_item = True
                print('Item {} has illegal slot value: {}'.format(item_name, properties['slot']))

        if invalid_item:
            exit(1)


class Stats:
    attack_power = 0
    crit = 0
    hit = 0
    dodge = 0
    armor = 0

    def add_to_stats(self, item):
        self.attack_power += item['attack_power']
        self.attack_power += 2 * item['strength']

        self.crit += item['crit']
        self.crit += item['agility'] / 20

        self.hit += item['hit']

        self.dodge += item['dodge']

        self.armor += item['armor']


class Character:
    wardrobe = None
    stats = Stats()

    def set_current_items(self):
        self.wardrobe.set_current_items()

    def set_stats(self):
        for item in self.wardrobe.items:
            self.stats.add_to_stats(item)






