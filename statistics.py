def set_generator(sorted_items: dict):
    two_handers = None
    if 'two_hand' in sorted_items.keys():
        two_handers = sorted_items['two_hand'].copy()
        del sorted_items['two_hand']
    item_count = get_item_count_by_slot(sorted_items)
    current_items = [1] * item_count.__sizeof__()


def get_item_count_by_slot(sorted_items):
    item_count_dict = {}
    for slot in sorted_items.keys():
        if slot not in item_count_dict.keys():
            item_count_dict[slot] = 0
        item_count_dict[slot] += 1
    return item_count_dict
