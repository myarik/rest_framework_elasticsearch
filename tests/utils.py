from .test_data import DATA


def get_search_ids(search):
    return [int(item.meta.id) for item in search[:len(DATA)].execute()]