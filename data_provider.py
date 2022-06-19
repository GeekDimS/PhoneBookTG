import data_checker
import data_finder
import data_deleter
import file_worker
import data_former
import logger
import tkinter
from tkinter import *
from tkinter import messagebox

ADD_WINDOW_HEADER = "Добавление в базу"
FIND_WINDOW_HEADER = "Поиск в базе"
DELETE_WINDOW_HEADER = "Удаление из базы"
SWOW_ALL_RECORDS_HEADER = "Просмотр базы"

IMPORT_WINDOW_HEADER = "Импорт базы"
EXPORT_WINDOW_HEADER = "Экспорт базы"

def export_to_json():
    file_worker.export_from_csv_to_json_file()
    export_to_json_message = "Произведён экспорт базы из формата csv в формат json"
    logger.add_in_log(f'{EXPORT_WINDOW_HEADER}  {export_to_json_message}')
    show_data_message(EXPORT_WINDOW_HEADER, export_to_json_message)

def export_to_html():
    file_worker.export_from_csv_to_html_file()
    export_to_html_message = "Произведён экспорт базы из формата csv в формат html"
    logger.add_in_log(f'{EXPORT_WINDOW_HEADER}  {export_to_html_message}')
    show_data_message(EXPORT_WINDOW_HEADER, export_to_html_message)



def import_from_json():
    file_worker.import_from_json_to_csv_file()
    import_from_json_to_csv_message = "Произведён импорт базы из формата json в формат csv"
    logger.add_in_log(f'{IMPORT_WINDOW_HEADER}  {import_from_json_to_csv_message}')
    show_data_message(IMPORT_WINDOW_HEADER, import_from_json_to_csv_message)


def import_from_html():
    file_worker.import_from_html_to_csv_file()
    import_from_html_to_csv_message = "Произведён импорт базы из формата html в формат csv"
    logger.add_in_log(f'{IMPORT_WINDOW_HEADER}  {import_from_html_to_csv_message}')
    show_data_message(IMPORT_WINDOW_HEADER, import_from_html_to_csv_message)


def show_data_message(header, message):
    messagebox.showinfo(header, message)

def find_data_in_database(name, lastname, phone, data_finding_listbox):

    find_window_empty_message = "Найти данные не получится. Все поля поиска пустые."
    find_window_no_message = "Записи удовлетворяющие условию не найдены."
    find_window_yes_message = ""

    if not data_checker.check_data_empty_all(name.get(), lastname.get(), phone.get()):
        show_data_message(FIND_WINDOW_HEADER, find_window_empty_message)
        logger.add_in_log(f'{FIND_WINDOW_HEADER} "{name.get()}" "{lastname.get()}" "{phone.get()}" {find_window_empty_message}')
    else:
        lastname_string, name_string, phone_string = data_checker.data_correction(lastname.get(), name.get(), phone.get())
        data_finding = data_finder.find(name_string, lastname_string, phone_string)
        if len(data_finding) == 0:
            show_data_message(FIND_WINDOW_HEADER, find_window_no_message)
            logger.add_in_log(f'{FIND_WINDOW_HEADER} "{name.get()}" "{lastname.get()}" "{phone.get()}" {find_window_no_message}')
        else:
            find_window_yes_message = f'Найдено {len(data_finding)} записи(ей)'
            show_data_message(FIND_WINDOW_HEADER, find_window_yes_message)
            logger.add_in_log(f'{FIND_WINDOW_HEADER} "{name.get()}" "{lastname.get()}" "{phone.get()}" {find_window_yes_message}')
   
            data_finding_listbox.delete(0, END)
            data_finding_listbox.insert(END, "№  Фамилия               Имя                  Телефон")
            count = 1
            for finding in data_finding:
                data_finding_listbox.insert(END, data_former.format_string(count, finding))
                count += 1



def find_data_form_info(root, data_listbox):
    find_window = tkinter.Toplevel(root)
    find_window.title("Поиск данных")
    find_window.geometry("280x140")


    name = StringVar()
    lastname = StringVar()
    phone = StringVar()

    name_label = Label(find_window, text = "Введите имя:")
    lastname_label = Label(find_window, text = "Введите фамилию:")
    phone_label = Label(find_window, text = "Введите телефон:")
    plus_label = Label(find_window, text = "+")

    name_label.grid(row = 1, column = 0, sticky = "w")
    lastname_label.grid(row = 3, column = 0, sticky = "w")
    phone_label.grid(row = 5, column = 0, sticky = "w")
    plus_label.grid(row = 5, column = 1, sticky = "e")

    name_input = Entry(find_window, textvariable = name)
    lastname_input = Entry(find_window, textvariable = lastname)
    phone_input = Entry(find_window, textvariable = phone)
 
    name_input.grid(row = 1, column = 2, padx = 5, pady = 5)
    lastname_input.grid(row = 3, column = 2, padx = 5, pady = 5)
    phone_input.grid(row = 5, column = 2, padx = 5, pady = 5)

    #Значения по умолчанию
    name_input.insert(0, "")
    lastname_input.insert(0, "")
    phone_input.insert(0, "")


    message_button = Button(find_window, text = "   Найти   ", command = lambda: find_data_in_database(name , lastname , phone, data_listbox))
    message_button.grid(row = 7, column = 2, padx = 5, pady = 5)


def delete_data_from_database(name , lastname , phone, data_delete_listbox):
    delete_window_empty_message = "Удалить данные не получится. Ни одно из полей не заполнено."
    delete_window_no_message = "Записи, удовлетворяющие условию, не найдены."
    delete_window_yes_message = ""

    if not data_checker.check_data_empty_all(name.get(), lastname.get(), phone.get()):
        show_data_message(DELETE_WINDOW_HEADER, delete_window_empty_message)
        logger.add_in_log(f'{DELETE_WINDOW_HEADER} "{name.get()}" "{lastname.get()}" "{phone.get()}" {delete_window_empty_message}')
    else:
        lastname_string, name_string, phone_string = data_checker.data_correction(lastname.get(), name.get(), phone.get())
        delete_list = data_deleter.delete_data(name_string, lastname_string, phone_string)
        if len(delete_list) == 0:
            show_data_message(DELETE_WINDOW_HEADER, delete_window_no_message)
            logger.add_in_log(f'{DELETE_WINDOW_HEADER} "{name.get()}" "{lastname.get()}" "{phone.get()}" {delete_window_no_message}')
        else:
            delete_window_yes_message = f'Удалено {len(delete_list)} записи(ей)'
            show_data_message(DELETE_WINDOW_HEADER, delete_window_yes_message)
            logger.add_in_log(f'{DELETE_WINDOW_HEADER} "{name.get()}" "{lastname.get()}" "{phone.get()}" {delete_window_yes_message}')
   
            data_delete_listbox.delete(0, END)
            data_delete_listbox.insert(END, "№  Фамилия               Имя                  Телефон")
            count = 1
            for deleting in delete_list:
                data_delete_listbox.insert(END, data_former.format_string(count, deleting))
                count += 1


def delete_data_form_info(root, data_listbox):
    delete_window = tkinter.Toplevel(root)
    delete_window.title("Удаление данных")
    delete_window.geometry("280x140")

    name = StringVar()
    lastname = StringVar()
    phone = StringVar()

    name_label = Label(delete_window, text = "Введите имя:")
    lastname_label = Label(delete_window, text = "Введите фамилию:")
    phone_label = Label(delete_window, text = "Введите телефон:")
    plus_label = Label(delete_window, text = "+")

    name_label.grid(row = 1, column = 0, sticky = "w")
    lastname_label.grid(row = 3, column = 0, sticky = "w")
    phone_label.grid(row = 5, column = 0, sticky = "w")
    plus_label.grid(row = 5, column = 1, sticky = "e")

    name_input = Entry(delete_window, textvariable = name)
    lastname_input = Entry(delete_window, textvariable = lastname)
    phone_input = Entry(delete_window, textvariable = phone)
 
    name_input.grid(row = 1, column = 2, padx = 5, pady = 5)
    lastname_input.grid(row = 3, column = 2, padx = 5, pady = 5)
    phone_input.grid(row = 5, column = 2, padx = 5, pady = 5)

    #Значения по умолчанию
    name_input.insert(0, "")
    lastname_input.insert(0, "")
    phone_input.insert(0, "")

    message_button = Button(delete_window, text = "   Удалить   ", command = lambda: delete_data_from_database(name , lastname , phone, data_listbox))
    message_button.grid(row = 7, column = 2, padx = 5, pady = 5)


def add_data_to_file(name, lastname, phone, form_name):

    add_window_empty_message = "Добавить данные не получится. Не все поля заполнены."
    add_window_message = "Запись успешно добавлена\n"
    if not data_checker.check_data_empty_at_least_one(name.get(), lastname.get(), phone.get()):
        show_data_message(ADD_WINDOW_HEADER, add_window_empty_message) 
        logger.add_in_log(f'{ADD_WINDOW_HEADER} "{name.get()}" "{lastname.get()}" "{phone.get()}" {add_window_empty_message}')
    else:
        lastname_string, name_string, phone_string = data_checker.data_correction(lastname.get(), name.get(), phone.get())
        file_worker.add_to_csv_file([[ lastname_string, name_string, phone_string]])
        add_window_message += lastname_string + " " + name_string + " " + phone_string   
        show_data_message(ADD_WINDOW_HEADER, add_window_message)
        logger.add_in_log(f'{ADD_WINDOW_HEADER} {add_window_message}')

        name.set("")
        lastname.set("")
        phone.set("")
        form_name.destroy()

def add_data_form_info(root):
    add_window = tkinter.Toplevel(root)
    add_window.title("Добавить данные")
    add_window.geometry("280x140")

    name = StringVar()
    lastname = StringVar()
    phone = StringVar()

    name_label = Label(add_window, text = "Введите имя:")
    lastname_label = Label(add_window, text = "Введите фамилию:")
    phone_label = Label(add_window, text = "Введите телефон:")
    plus_label = Label(add_window, text = "+")

    name_label.grid(row = 1, column = 0, sticky = "w")
    lastname_label.grid(row = 3, column = 0, sticky = "w")
    phone_label.grid(row = 5, column = 0, sticky = "w")
    plus_label.grid(row = 5, column = 1, sticky = "e")

    name_input = Entry(add_window, textvariable = name)
    lastname_input = Entry(add_window, textvariable = lastname)
    phone_input = Entry(add_window, textvariable = phone)

    name_input.grid(row = 1, column = 2, padx = 5, pady = 5)
    lastname_input.grid(row = 3, column = 2, padx = 5, pady = 5)
    phone_input.grid(row = 5, column = 2, padx = 5, pady = 5)

    #Значения по умолчанию
    name_input.insert(0, "")
    lastname_input.insert(0, "")
    phone_input.insert(0, "")

    reg_phone = add_window.register(data_checker.check_symbol_phone)
    phone_input.config(validate = "key", validatecommand = (reg_phone, "%P"))

    reg_name_lastname = add_window.register(data_checker.check_symbol_name_lastname)
    lastname_input.config(validate = "key", validatecommand = (reg_name_lastname, "%P"))
    name_input.config(validate = "key", validatecommand = (reg_name_lastname, "%P"))

    message_button = Button(add_window, text = "Добавить", command = lambda: add_data_to_file(name, lastname, phone, add_window))
    message_button.grid(row = 7, column = 2, padx = 5, pady = 5)

def show_all_data(data_listbox):
    all_data = file_worker.read_from_csv_file()
    show_all_data_message = f'В базе данных {len(all_data)} записи(ей)'
    show_data_message(SWOW_ALL_RECORDS_HEADER, show_all_data_message) 

    data_listbox.delete(0, END)
    data_listbox.insert(END, "№  Фамилия               Имя                  Телефон")
    count = 1
    for data in all_data:
        data_listbox.insert(END, data_former.format_string(count, data_former.from_dict_to_value_list(data)))
        count += 1
    logger.add_in_log('Показаны все записи из телефонной книги - ' + show_all_data_message)


def main_menu():
    root = Tk()
    root.title("Работа с телефонным справочником")
    root.geometry("450x250")

    scrollbar = Scrollbar(root)
    scrollbar.pack(side = RIGHT, fill = Y)
    
    data_listbox = Listbox(root, yscrollcommand=scrollbar.set, width = 70)

    message_button = Button(text = "Показать все данные",  background="#C0C0C0", command = lambda: show_all_data(data_listbox))
    message_button.pack(side = TOP, fill = X)
    data_listbox.pack(side = LEFT, fill = Y)

    scrollbar.config(command = data_listbox.yview)
 
    main_menu = Menu() 
    data_menu = Menu()
    export_menu = Menu()
    import_menu = Menu()

    main_menu.add_cascade(label = "Данные", menu = data_menu)
    main_menu.add_cascade(label = "Экспорт данных", menu = export_menu)
    main_menu.add_cascade(label = "Импорт данных", menu = import_menu)

    data_menu.add_command(label = "Добавить", command = lambda: add_data_form_info(root))
    data_menu.add_command(label = "Найти", command = lambda: find_data_form_info(root, data_listbox))
    data_menu.add_command(label = "Удалить", command = lambda: delete_data_form_info(root, data_listbox))

    export_menu.add_command(label = "В json формат", command = export_to_json)
    export_menu.add_command(label = "В html формат", command = export_to_html)
    
    import_menu.add_command(label = "Из json формата", command = import_from_json)
    import_menu.add_command(label = "Из html формата", command = import_from_html)



    # root.config(menu = main_menu)
 
    # root.mainloop()
 
#main_menu()