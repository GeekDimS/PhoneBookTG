def delete_extra_spaces(string_original):
    string_original = string_original.strip()
    return string_original
    
def first_capital_letter(string_original):
    string_result = string_original.lower()
    if string_result != "":
        string_result = string_result[0].upper() + string_result[1 : ]
    return string_result

def data_correction(*data):
    for item in data:
        item = delete_extra_spaces(item)

    lastname, name, phone = data
    name = first_capital_letter(name)
    lastname = first_capital_letter(lastname)
    phone = '+' + phone
    return (lastname, name, phone)


def check_symbol_phone(symbol):
    if symbol.isdigit() or symbol == "":
        return True
    else:
        return False


def check_symbol_name_lastname(symbol):
    if symbol.isalpha() or symbol == "":
        return True
    else:
        return False

def check_data_empty_all(*data):
    for item in data:
        if item != "":
            return True
    return False


def check_data_empty_at_least_one(*data):
    for item in data:
        if item == "":
            return False
    return True

