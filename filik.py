from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
import data_provider
import data_checker
import data_finder
import data_deleter
import file_worker
import data_former
import logger

# pip install python-telegram-bot - загрузить библиотеку
# Удалить!!! Строка только для проверки работы Гит

path_file_token = 'token.txt'    # Запишите токен своего Телеграм бота в текстовый файл по такому пути!!!
with open(path_file_token, 'r') as data:
    for line in data:
        str_token = line

bot = Bot(token=str_token)
updater = Updater(token=str_token, use_context=True)
dispatcher = updater.dispatcher

NAME, LASTNAME, PHONE = range(3) #константы этапов разговоров

ADD_WINDOW_HEADER = "Добавление в базу"
FIND_WINDOW_HEADER = "Поиск в базе"
DELETE_WINDOW_HEADER = "Удаление из базы"
SWOW_ALL_RECORDS_HEADER = "Просмотр базы"

IMPORT_WINDOW_HEADER = "Импорт базы"
EXPORT_WINDOW_HEADER = "Экспорт базы"

FIND_ACTION = "Find"
DELETE_ACTION = "Delete"


def start(update, context):
    arg = context.args
    if not arg:
        context.bot.send_message(update.effective_chat.id, "Привет, я телефонный справочник\nВот список моих возможностей:")
        context.bot.send_message(update.effective_chat.id, "/allphones -- показать списое всех абонентов\n"
                                                            "/addphone -- добавить абонента\n"
                                                            "/deletephone -- удалить абонента\n"
                                                            "/findphone -- найти абонента\n"
                                                            "/exporttojson -- экспортировать базу данных в json формат\n"
                                                            "/exporttohtml -- экспортировать базу данных в html формат\n"
                                                            "/importfromjson -- импортировать базу данных из json формата\n"
                                                            "/importfromhtml -- импортировать базу данных из html формата\n")
    else:
        context.bot.send_message(update.effective_chat.id, f"{' '.join(arg)}")


def info(update, context):
    context.bot.send_message(update.effective_chat.id, "Меня создала компанда из курса 'Разработчик!'")


def message(update, context):
    text = update.message.text
    if text.lower() == 'привет':
        context.bot.send_message(update.effective_chat.id, 'И тебе привет..')
    else:
        context.bot.send_message(update.effective_chat.id, 'я тебя не понимаю')


def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, 'Ты несешь какую-то дичь...')


def export_to_json(update, context):
    file_worker.export_from_csv_to_json_file()
    export_to_json_message = "Произведён экспорт базы из формата csv в формат json"
    logger.add_in_log(f'{EXPORT_WINDOW_HEADER}  {export_to_json_message}')
    context.bot.send_message(update.effective_chat.id, EXPORT_WINDOW_HEADER + "... " + export_to_json_message)


def export_to_html(update, context):
    file_worker.export_from_csv_to_html_file()
    export_to_html_message = "Произведён экспорт базы из формата csv в формат html"
    logger.add_in_log(f'{EXPORT_WINDOW_HEADER}  {export_to_html_message}')
    context.bot.send_message(update.effective_chat.id, EXPORT_WINDOW_HEADER + "... " + export_to_html_message)

def import_from_json(update, context):
    file_worker.import_from_json_to_csv_file()
    import_from_json_to_csv_message = "Произведён импорт базы из формата json в формат csv"
    logger.add_in_log(f'{IMPORT_WINDOW_HEADER}  {import_from_json_to_csv_message}')
    context.bot.send_message(update.effective_chat.id, IMPORT_WINDOW_HEADER + "... " + import_from_json_to_csv_message)


def import_from_html(update, context):
    file_worker.import_from_html_to_csv_file()
    import_from_html_to_csv_message = "Произведён импорт базы из формата html в формат csv"
    logger.add_in_log(f'{IMPORT_WINDOW_HEADER}  {import_from_html_to_csv_message}')
    context.bot.send_message(update.effective_chat.id, IMPORT_WINDOW_HEADER + "... " + import_from_html_to_csv_message)


def show_all_data(update, context):
    all_data = file_worker.read_from_csv_file()
    show_all_data_message = f'В базе данных {len(all_data)} записи(ей)'

    context.bot.send_message(update.effective_chat.id, SWOW_ALL_RECORDS_HEADER + ' ' + show_all_data_message)
    context.bot.send_message(update.effective_chat.id, "№  Фамилия               Имя                  Телефон")
    count = 1
    for data in all_data:
        context.bot.send_message(update.effective_chat.id, data_former.format_string(count, data_former.from_dict_to_value_list(data)))
        count += 1
    logger.add_in_log('Показаны все записи из телефонной книги - ' + show_all_data_message)

def delete_data_from_database(update, name_loc, lastname_loc, phone_loc):
    delete_window_empty_message = "Удалить данные не получится. Ни одно из полей не заполнено."
    delete_window_no_message = "Записи, удовлетворяющие условию, не найдены."
    delete_window_yes_message = ""

    update.message.reply_text(DELETE_WINDOW_HEADER + '... ' + delete_window_yes_message)

    if not data_checker.check_data_empty_all(name_loc, lastname_loc, phone_loc):
        update.message.reply_text(DELETE_WINDOW_HEADER + '... ' + delete_window_empty_message)
        logger.add_in_log(f'{DELETE_WINDOW_HEADER} "{name_loc}" "{lastname_loc}" "{phone_loc}" {delete_window_empty_message}')
    else:
        lastname_string, name_string, phone_string = data_checker.data_correction(lastname_loc, name_loc, phone_loc)
        delete_list = data_deleter.delete_data(name_string, lastname_string, phone_string)
        if len(delete_list) == 0:
            update.message.reply_text(DELETE_WINDOW_HEADER + '... ' + delete_window_no_message)
            logger.add_in_log(f'{DELETE_WINDOW_HEADER} "{name_loc}" "{lastname_loc}" "{phone_loc}" {delete_window_no_message}')
        else:
            delete_window_yes_message = f'Удалено {len(delete_list)} записи(ей)'
            update.message.reply_text(DELETE_WINDOW_HEADER + '... ' + delete_window_yes_message)
            logger.add_in_log(f'{DELETE_WINDOW_HEADER} "{name_loc}" "{lastname_loc}" "{phone_loc}" {delete_window_yes_message}')
   

            update.message.reply_text("№  Фамилия               Имя                  Телефон")
            count = 1
            for deleting in delete_list:
                update.message.reply_text(data_former.format_string(count, deleting))
                count += 1

def find_data_in_database(update, name_loc, lastname_loc, phone_loc):

    find_window_empty_message = "Найти данные не получится. Все поля поиска пустые."
    find_window_no_message = "Записи удовлетворяющие условию не найдены."
    find_window_yes_message = ""

    if not data_checker.check_data_empty_all(name_loc, lastname_loc, phone_loc):
        update.message.reply_text(FIND_WINDOW_HEADER + '... ' + find_window_empty_message)
        logger.add_in_log(f'{FIND_WINDOW_HEADER} "{name_loc}" "{lastname_loc}" "{phone_loc}" {find_window_empty_message}')
    else:
        lastname_string, name_string, phone_string = data_checker.data_correction(lastname_loc, name_loc, phone_loc)
        data_finding = data_finder.find(name_string, lastname_string, phone_string)
        if len(data_finding) == 0:
            update.message.reply_text(FIND_WINDOW_HEADER + '... ' +  find_window_no_message)
            logger.add_in_log(f'{FIND_WINDOW_HEADER} "{name_loc}" "{lastname_loc}" "{phone_loc}" {find_window_no_message}')
        else:
            find_window_yes_message = f'Найдено {len(data_finding)} записи(ей)'
            update.message.reply_text(FIND_WINDOW_HEADER + '... ' +  find_window_yes_message)
            logger.add_in_log(f'{FIND_WINDOW_HEADER} "{name_loc}" "{lastname_loc}" "{phone_loc}" {find_window_yes_message}')

            update.message.reply_text("№  Фамилия               Имя                  Телефон")
            count = 1
            for finding in data_finding:
                update.message.reply_text(data_former.format_string(count, finding))
                count += 1


def add_phone(update, context):
    add_window_empty_message = "Добавить данные не получится. Не все поля заполнены."
    add_window_message = "Запись успешно добавлена\n"

    arg = context.args
    name, lastname, phone = arg
    if not data_checker.check_data_empty_at_least_one(name, lastname, phone):
        context.bot.send_message(update.effective_chat.id, ADD_WINDOW_HEADER +' '+ add_window_empty_message) 
        logger.add_in_log(f'{ADD_WINDOW_HEADER} "{name.get()}" "{lastname.get()}" "{phone.get()}" {add_window_empty_message}')
    else:
        lastname_string, name_string, phone_string = data_checker.data_correction(lastname, name, phone)
        file_worker.add_to_csv_file([[ lastname_string, name_string, phone_string]])
        add_window_message += lastname_string + " " + name_string + " " + phone_string   
        context.bot.send_message(update.effective_chat.id, ADD_WINDOW_HEADER +'... '+ add_window_message)
        logger.add_in_log(f'{ADD_WINDOW_HEADER} {add_window_message}')    

def input_data_delete(update, context):

    global function    
    function = DELETE_ACTION
    context.bot.send_message(update.effective_chat.id, 'Введите имя для удаления или отправьте /skip для пропуска')
    return NAME


def input_data_find(update, context):
    global function   
    function = FIND_ACTION
    context.bot.send_message(update.effective_chat.id, 'Введите имя для поиска или отправьте /skip для пропуска')
    return NAME

def input_name(update, context):
    global name
    name = update.message.text
    # print(name)
    if function == FIND_ACTION:
        update.message.reply_text('Введите фамилию для поиска или отправьте /skip для пропуска')
    elif function == DELETE_ACTION:
        update.message.reply_text('Введите фамилию для удаления или отправьте /skip для пропуска')
    return LASTNAME

def skip_name(update, _):
    global name
    name = ""
    update.message.reply_text('Ввод имени был пропущен')
    if function == FIND_ACTION:
        update.message.reply_text('Введите фамилию для поиска или отправьте /skip для пропуска')
    elif function == DELETE_ACTION:
        update.message.reply_text('Введите фамилию для удаления или отправьте /skip для пропуска')
    return LASTNAME


def input_lastname(update, _):   
    global lastname
    lastname = update.message.text
    # print(lastname)
    if function == FIND_ACTION:
        update.message.reply_text('Введите телефон для поиска или отправьте /skip для пропуска')
    elif function == DELETE_ACTION:
        update.message.reply_text('Введите телефон для удаления или отправьте /skip для пропуска')
    return PHONE

def skip_lastname(update, _):
    global lastname
    lastname = ""
    update.message.reply_text('Ввод фамилии был пропущен')
    if function == FIND_ACTION:
        update.message.reply_text('Введите телефон для поиска или отправьте /skip для пропуска')
    elif function == DELETE_ACTION:
        update.message.reply_text('Введите телефон для удаления или отправьте /skip для пропуска')
    return PHONE

def input_phone(update, _):   
    global phone
    phone = update.message.text
    # print(phone)
    update.message.reply_text('Спасибо за ввод данных, обрабатываю ваш запрос...')
    if function == FIND_ACTION:
        find_data_in_database(update, name, lastname, phone)
    elif function == DELETE_ACTION:
        delete_data_from_database(update, name, lastname, phone)
    return ConversationHandler.END

def skip_phone(update, _):
    global phone
    phone = ""
    update.message.reply_text('Ввод телефона был пропущен')
    update.message.reply_text('Спасибо за ввод данных, обрабатываю ваш запрос...')
    if function == FIND_ACTION:
        find_data_in_database(update, name, lastname, phone)
    elif function == DELETE_ACTION:
        delete_data_from_database(update, name, lastname, phone)
    return ConversationHandler.END

def cancel(update, _):
    return ConversationHandler.END

conv_handler_find = ConversationHandler(
    
    entry_points = [CommandHandler('findphone', input_data_find), CommandHandler('deletephone', input_data_delete)],
    states = {
        NAME: [CommandHandler('skip', skip_name), MessageHandler(Filters.text, input_name)],
        LASTNAME: [CommandHandler('skip', skip_lastname), MessageHandler(Filters.text, input_lastname)],
        PHONE: [CommandHandler('skip', skip_phone), MessageHandler(Filters.text, input_phone)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
# message_handler = MessageHandler(Filters.text, message)
# unknown_handler = MessageHandler(Filters.command, unknown) #/game

all_view_handler = CommandHandler('allphones', show_all_data)
addphone_handler = CommandHandler('addphone', add_phone)
export_to_json_handler = CommandHandler('exporttojson', export_to_json)
export_to_html_handler = CommandHandler('exporttohtml', export_to_html)
import_from_json_handler = CommandHandler('importfromjson', import_from_json)
import_from_html_handler  = CommandHandler('importfromhtml', import_from_html)

#input_data_find_handler = CommandHandler('findphone', input_data_find)
#input_data_delete_handler = CommandHandler('deletephone', input_data_delete)


dispatcher.add_handler(addphone_handler)
dispatcher.add_handler(all_view_handler)
dispatcher.add_handler(export_to_json_handler)
dispatcher.add_handler(export_to_html_handler)
dispatcher.add_handler(import_from_json_handler)
dispatcher.add_handler(import_from_html_handler)
# dispatcher.add_handler(input_data_find_handler)
# dispatcher.add_handler(input_data_delete_handler)
dispatcher.add_handler(conv_handler_find)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
# dispatcher.add_handler(unknown_handler)
# dispatcher.add_handler(message_handler)


print("server_started")

updater.start_polling()
updater.idle()