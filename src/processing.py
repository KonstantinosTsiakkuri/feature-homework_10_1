def filter_by_state(dict_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция принимает список словарей и возвращает новый список, у которых ключ соответствует указанному значению"""
    new_dict_list = []
    for dictionary in dict_list:
        if dictionary["state"] == state:
            new_dict_list.append(dictionary)
    return new_dict_list


dict_list = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]
state = input()
print(filter_by_state(dict_list, state))


def sort_by_date(dict_list: list[dict], reverse: bool = True) -> list[dict]:
    """Функция, которая принимает список словарей и возвращает новый список, отсортированный по дате"""
    new_dict = sorted(dict_list, key=lambda x: x["date"], reverse=reverse)
    return new_dict


dict_list = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]
print(sort_by_date(dict_list, reverse=True))
