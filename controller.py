"""
Этот модуль на данный момент не используется в проекте, поскольку перешли с консольного на оконное
приложение. Оставлен для "истории". 
"""
from distutils.log import error
from statistics import mode
import data_finder
import data_provider
import file_worker
import data_former
from waiting import wait


def run():
    # error = False
    dpf_req = data_provider.dpf1 # Ф-я запроса данных от пользователя Вход: (Void).Выход: (mode,('lastname','name','phone'))
    # mode: 'add'or'search'or'end'or'export html'of'export_json'or'import_html'or'import_json'
    dpf_out = data_provider.dpf2 # Ф-я вывода(печати) найденных данных и сама выводит сообщение меню  Вход: ([('lastname','name','phone'),('lastname2','name2','phone2'),...]) Выход:(Void)
    dfm_list_read = data_former.dfm1 # Ф-я формирования найденных данных от data_finder из вида csv в список кортежей строк для передачи в data_provider Вход:(?список строк в формате csv?) Выход:([('lastname','name','phone'),('lastname2','name2','phone2'),...])
    dfm_list_wriite = data_former.dfm2 # Ф-я формирования строки для записи в файл из ответа от data_provider.dpf1 Вход: ('lastname','name','phone') Выход:(?строка в формате csv?)
    dfn_find = data_finder.find # Ф-я поиска данных в файле Вход: ('lastname','name','phone') Выход: (?список строк в формате csv?)
    fw_read_next = file_worker.fw1 # Ф-я чтения следующей строки данных Вход:(Void) Выход: ('End # достигнут конец файла #', (?строка в формате csv?))
    fw_write = file_worker.add_to_csv_file # Ф-я записи новой строки в конец файла Вход:(?строка в формате csv?) Выход: (Void)
    fw_exp_html = file_worker.export_from_csv_to_html_file
    fw_exp_json = file_worker.export_from_csv_to_json_file
    # fw_imp_html = file_worker.???
    # fw_imp_json = file_worker.???

    ## mode_work, list_data = dpf_req()
    global mode_work
    global list_data
    mode_work, list_data = '',''        # Инициализация режима работы и рабочего списка
    data_provider.main_menu()
    


    if mode_work == 'end':
        return False
    elif mode_work == 'add':
        if not fw_write(list_data):  # Возможны проблемы - нужен список списков
            error('Ошибка добавления записи в файл')
            # Сделать возвращаемое значение из file_worker.add_to_csv_file True, если нет ошибок
        return True
    elif mode_work == 'search':
        # coding here
        data_fainding = dfn_find(list_data)  # Передаём данные для поиска в базе
        dpf_out(data_fainding)          # Передаём результат в privider для вывода пользователю 
        return True
    elif mode_work == 'export_html':
        fw_exp_html()
        return True
    elif mode_work == 'export_json':
        fw_exp_json()
        return True
    # elif mode_work == 'import_html':
    #     # coding here
    #     return
    # elif mode_work == 'import_json':
    #     # coding here
    #     return
    else:
        error('Ошибка выполнения программы')         # Ф-я обработки ошибок.
        # Написать! Выводит сообщение об ошибке с помощью provider
    