from collections import defaultdict


def group_by_value(objects, value):
    grouped_dict = defaultdict(list)

    for obj in objects:
        obj_id = obj[value]
        grouped_dict[obj_id].append(obj)

    return grouped_dict
