import logging
import requests, json

# Старт - стартуем. Далее - идет вопрос (и варианты ответов). Для начала - делаем вопрос с 4-мя кнопками. Далее - смотрим правильные ответы.

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

reg_list = ["",""]

account = 0
condition = 0

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}

total_n = 0
n_question = 0
n_right_answer = 0
right_answer_total = 0
n_question_total = 0 

check_strings = ["Your input is correct","Your input is empty","Parameter of command is not digit"]



def question(update,context):
    global HEADERS,n_right_answer,n_question,total_n
    total_n = 0
    n_question = 0
    n_right_answer = 0
    right_answer_total = 0
    n_question_total = 0 
    r = requests.get('https://innovations.kh.ua/quiz/list/?author_id=0&n='+str(n_question),headers=HEADERS)
    element = r.json()
    total_n = element['total_n']
    n_right_answer = element['n_right_answer_arr'][0]
    keyboard = key_buttons(element['a1_arr'][0],element['a2_arr'][0],element['a3_arr'][0],element['a4_arr'][0])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(element['question_arr'][0], reply_markup=reply_markup)


def question1(update,context):
    global HEADERS,n_right_answer,n_question,total_n
    r = requests.get('https://innovations.kh.ua/quiz/list/?author_id=0&n='+str(n_question),headers=HEADERS)
    element = r.json()
    n_right_answer = element['n_right_answer_arr'][0]

    keyboard = key_buttons(element['a1_arr'][0],element['a2_arr'][0],element['a3_arr'][0],element['a4_arr'][0])
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=str(element['title_arr'][0]),reply_markup=reply_markup)
    # update.message.reply_text(element['question_arr'][0], reply_markup=reply_markup)

def result(update,context):
    global right_answer_total
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=f"{str(right_answer_total)} from {str(total_n)}")



def check(string_in):
    n=0
    elements = string_in.split(' ')

    if not len(string_in) > 0:
        n=1
    elif not string_in.isdigit():
        n=2
    return n

def key_buttons(text1,text2,text3,text4):

    reg_title = [text1,text2]
    reg_code = ["1","2"]
    key_lst1 = []    
    for i in range(len(reg_title)):
        key_lst1.append(InlineKeyboardButton(reg_title[i], callback_data=reg_code[i]))
    reg_title = [text3,text4]
    reg_code = ["3","4"]
    key_lst2 = []    
    for i in range(len(reg_title)):
        key_lst2.append(InlineKeyboardButton(reg_title[i], callback_data=reg_code[i]))
    kb = [key_lst1,key_lst2]

    return kb

def start(update: Update, context: CallbackContext) -> None:
    question(update,context)

def button(update: Update, context: CallbackContext) -> None:
    global condition,n_question,right_answer_total
    query = update.callback_query
    query.answer()
    if query.data == str(n_right_answer):
        query.edit_message_text(text=f"Правильный ответ")
        right_answer_total += 1
    else:
        query.edit_message_text(text=f"Неправильный ответ")
    print(n_question)
    n_question +=1
    print(n_question)
    if int(n_question)<int(total_n):
        question1(update,context)
    else:
        result(update,context)

def echo(update, context):
    global condition, account
    string_in = update.message.text

    if string_in == '/start':
        string_out = 'Hello! This is own finances bot!'
    elif condition == 1:
        condition = 0
        if not check(string_in):
            account = account + int(string_in)
            string_out = "Состояние вашего счета: "+str(account)
        else:
            string_out = check_strings[check(string_in)]

    elif condition == 2:
        if not check(string_in):
            account = account - int(string_in)
            string_out = "Состояние вашего счета: "+str(account)
        else:
            string_out = check_strings[check(string_in)]
    else:
        string_out = string_in


    keyboard = key_buttons()
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(string_out,reply_markup=reply_markup)


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    updater = Updater("2034824924:AAFc0q0PYPezeZ6G5kE10uBWhWSurKks-8A")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()