import numpy as np
import bisect
from items import *


def get_item_iterator(sorted_items: dict, allow_kots_and_kiss_together=False):
    items_list = list(sorted_items.values())
    if not allow_kots_and_kiss_together:
        remove_kots_and_kiss_combo(items_list)
    item_count = get_item_count_by_slot(sorted_items)
    current_set_indeces = [0] * sorted_items.keys().__len__()
    sets_left_to_explore = True

    while sets_left_to_explore:
        current_set = []
        for i_gear_type, i_piece in enumerate(current_set_indeces):
            if type(items_list[i_gear_type][i_piece]) is list:
                # rings, trinkets and weapons are a list of pairs of items
                # so, extend
                current_set.extend(items_list[i_gear_type][i_piece])
            else:
                # the other items are dicts, append
                current_set.append(items_list[i_gear_type][i_piece])

        yield current_set

        sets_left_to_explore = increase_index_and_check_if_more_sets(
            current_set_indeces, item_count)


def remove_kots_and_kiss_combo(items_list):
    slot_nr_to_remove = None
    item_nr_to_remove = None
    for slot_nr, items in enumerate(items_list):
        for item_nr, item in enumerate(items):
            if type(item) is list:
                if (Items.kiss_of_the_spider in item
                        and Items.slayers_crest in item):
                    slot_nr_to_remove = slot_nr
                    item_nr_to_remove = item_nr
    if slot_nr_to_remove is not None:
        del items_list[slot_nr_to_remove][item_nr_to_remove]


def get_nr_of_set_combinations(items_by_slot):
    nr_sets = np.prod([len(val) for val in items_by_slot.values()])
    return nr_sets


def increase_index_and_check_if_more_sets(current_set_indeces, item_count):
    for i_position, _ in enumerate(current_set_indeces):
        if current_set_indeces[i_position] + 1 < item_count[i_position]:
            current_set_indeces[i_position] += 1
            return True
        else:
            current_set_indeces[i_position] = 0
    return False


def no_index_too_high(current_values, max_values):
    for key, counts in zip(current_values.items(), max_values.items()):
        print(key)
        print(counts)
    return False


def get_item_count_by_slot(sorted_items):
    item_count_list = []
    for slot_key in sorted_items.keys():
        item_count_list.append(sorted_items[slot_key].__len__())
    return item_count_list


def get_zeros_dict_from_template(item_count):
    output = {}
    for key, _ in item_count.items():
        output[key] = 1
    return output


class Secretary:
    def __init__(self, tps_list_length):
        # row 1 has tps, row 2 corresponding set_nr
        self.top_tps_with_setnr_list = np.arange(tps_list_length)
        temp_second_row = np.ones(tps_list_length) * -1
        self.top_tps_with_setnr_list = np.vstack((self.top_tps_with_setnr_list,
                                                  temp_second_row))
        self.set_nr_to_set_dict = {}
        self.tps_list_length = tps_list_length

    def report_tps(self, tps, set_nr, set_names):

        if tps > self.top_tps_with_setnr_list[0][0]:
            # delete nr 0 first
            delete_set = '{}'.format(self.top_tps_with_setnr_list[0][1])
            if delete_set in self.set_nr_to_set_dict.keys():
                del self.set_nr_to_set_dict[delete_set]
            self.top_tps_with_setnr_list = np.delete(self.top_tps_with_setnr_list,
                                                     0, axis=1)

            if tps > self.top_tps_with_setnr_list[0][-1]:
                self.top_tps_with_setnr_list = np.hstack((self.top_tps_with_setnr_list,
                                                          [[tps], [set_nr]]))
            else:
                insertion_index = np.searchsorted(self.top_tps_with_setnr_list[0],
                                                  tps, side='right')
                self.top_tps_with_setnr_list = np.insert(self.top_tps_with_setnr_list,
                                                         insertion_index, [tps, set_nr],
                                                         axis=1)

            add_set = '{}'.format(set_nr)
            self.set_nr_to_set_dict[add_set] = set_names

    def give_report(self):
        self.print_best_n_sets()

        appearances_per_slot_and_item = {s: {} for s in Slots}
        for i in range(self.top_tps_with_setnr_list.shape[1]):
            set_string = '{:.0f}'.format(self.top_tps_with_setnr_list[1][i])
            item_set = self.set_nr_to_set_dict[set_string]
            for item in item_set:
                if item.name not in appearances_per_slot_and_item[item.slot].keys():
                    appearances_per_slot_and_item[item.slot][item.name] = 0
                appearances_per_slot_and_item[item.slot][item.name] += 1

        print('Occurrences:')
        for slot in appearances_per_slot_and_item.keys():
            print('### {} ###'.format(slot))
            for name, nr in appearances_per_slot_and_item[slot].items():
                print('    {:<40} {:.0f}%'.format(name, 100*nr/self.tps_list_length))

        print(self.top_tps_with_setnr_list[0])

    def print_best_n_sets(self, n=3):
        for i in range(n):
            set_string = '{:.0f}'.format(self.top_tps_with_setnr_list[1][-1-i])
            print('## Set nr {}, {:.2f}tps ###'
                  .format(i+1, self.top_tps_with_setnr_list[0][-1-i]))
            for item in self.set_nr_to_set_dict[set_string]:
                print('{:<20} {}'.format(item.slot, item.name))
            print()



























