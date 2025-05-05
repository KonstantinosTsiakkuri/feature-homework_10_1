def mask_account_card(number_type: str) -> str:
    """Функция принимает тип и номер карты или счета и возвращает строку с замаскированным номером"""
    if "Счет" in number_type:
        number_mask = "**" + number_type[-4:]
        return f"Счет {number_mask}"
    else:
        number_type_splited = number_type.split()
        card_type_sep = " ".join(number_type_splited[:-1])
        card_number_sep = number_type_splited[-1]
        number_mask = "" + card_number_sep[0:4] + " " + card_number_sep[4:6] + "** **** " + card_number_sep[-4:]
        return f"{card_type_sep} {number_mask}"


number_type = input()
print(mask_account_card(number_type))
