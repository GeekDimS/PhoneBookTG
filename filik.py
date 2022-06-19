from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import data_provider
import data_checker
import data_finder
import data_deleter
import file_worker
import data_former
import logger

# pip install python-telegram-bot - загрузить библиотеку

path_file_token = 'C:/token.txt'    # Запишите токен своего Телеграм бота в текстовый файл по такому пути!!!
with open(path_file_token, 'r') as data:
    for line in data:
        str_token = line

bot = Bot(token=str_token)
updater = Updater(token=str_token, use_context=True)
dispatcher = updater.dispatcher


ADD_WINDOW_HEADER = "Добавление в базу"
FIND_WINDOW_HEADER = "Поиск в базе"
DELETE_WINDOW_HEADER = "Удаление из базы"
SWOW_ALL_RECORDS_HEADER = "Просмотр базы"

IMPORT_WINDOW_HEADER = "Импорт базы"
EXPORT_WINDOW_HEADER = "Экспорт базы"


def start(update, context):
    arg = context.args
    if not arg:
        context.bot.send_message(update.effective_chat.id, "Привет")
    else:
        context.bot.send_message(update.effective_chat.id, f"{' '.join(arg)}")


def info(update, context):
    context.bot.send_message(update.effective_chat.id, "Меня создала компания GB!")


def message(update, context):
    text = update.message.text
    if text.lower() == 'привет':
        context.bot.send_message(update.effective_chat.id, 'И тебе привет..')
    else:
        context.bot.send_message(update.effective_chat.id, 'я тебя не понимаю')


def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, 'Ты несешь какую-то дичь...')



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
        context.bot.send_message(update.effective_chat.id, ADD_WINDOW_HEADER +' '+ add_window_message)
        logger.add_in_log(f'{ADD_WINDOW_HEADER} {add_window_message}')    



start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
message_handler = MessageHandler(Filters.text, message)
unknown_handler = MessageHandler(Filters.command, unknown) #/game

all_view_handler = CommandHandler('allphones', show_all_data)
addphone_handler = CommandHandler('addphone', add_phone)


dispatcher.add_handler(addphone_handler)
dispatcher.add_handler(all_view_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(message_handler)


print("server_started")

updater.start_polling()
updater.idle()