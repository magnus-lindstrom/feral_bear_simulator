def get_item_iterator(sorted_items: dict):
    # TODO: set separate combinations of rings/trinkets/weapons and import them to onee
    #       slot
    two_handers = None
    if 'two_hand' in sorted_items.keys():
        two_handers = sorted_items['two_hand'].copy()
        del sorted_items['two_hand']
    items_list = list(sorted_items.values())
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

    # if there are two handers, swap them with mh+oh
    if two_handers is not None:
        if 'main_hand' in sorted_items.keys():
            del sorted_items['main_hand']
        if 'off_hand' in sorted_items.keys():
            del sorted_items['off_hand']
        sorted_items['two_hand'] = two_handers

        items_list = list(sorted_items.values())
        item_count = get_item_count_by_slot(sorted_items)
        current_set_indeces = [0] * sorted_items.keys().__len__()
        sets_left_to_explore = True

        while sets_left_to_explore:
            current_set = []
            for i_gear_type, i_piece in enumerate(current_set_indeces):
                current_set.append(items_list[i_gear_type][i_piece])
            yield current_set

            sets_left_to_explore = increase_index_and_check_if_more_sets(
                current_set_indeces, item_count)


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