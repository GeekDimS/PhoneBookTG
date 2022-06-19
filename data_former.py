
def format_string(number, data_list):
    length_number = 5
    length_item = 20
    result = str(number) + " " * (length_number - len(str(number)))
    for item in data_list:
        result += item + " " * (length_item - len(str(item)))
    return result


def from_dict_to_value_list(dict):
    return [dict['Lastname'], dict['Name'], dict['Phone']]

def return_first_word(separator, string_original):
    result = ""
    list_from_string_original =  string_original.split(separator)
    if len(list_from_string_original) > 1:
        for symbol in list_from_string_original[1]:
            if symbol.isalpha():
                result += symbol
            else:
                break
    return result
 

def return_phone_number(separator, string_original):
    result = ""
    list_from_string_original =  string_original.split(separator)
    if len(list_from_string_original) > 1:
        result = list_from_string_original[1][ : -1]
    return result


def from_html_to_value_list(html_string):   
    return [return_first_word("Lastname: ", html_string), return_first_word("Name: ", html_string), return_phone_number("Phone: ", html_string)]