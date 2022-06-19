import file_worker as fw

def delete_data(name, lname, phnumber):
    #not_eof = True
    res = []
    res_to_bd = []
    data_base = fw.read_from_csv_file()         # Считываем данные из файла. Данные в виде списка словарей
    #while not_eof:      # Пока нет конца файла

    for item in data_base:      # Пока не кончились записи в базе
        lname_f, name_f, phnumber_f = item.values()     # Распаковываем строку словаря        

        if (lname == lname_f and name == '') or (name == name_f and lname == '') or (lname == lname_f and name == name_f) or (phnumber == phnumber_f):    # Если есть совпадение хоть по одному полю или по двум с именами
            res.append([lname_f, name_f, phnumber_f])   # то добавляем запись в результирующий список
        else:  
            res_to_bd.append([lname_f, name_f, phnumber_f])   # то добавляем запись в результирующий список
    fw.write_to_csv_file(res_to_bd)
    return res