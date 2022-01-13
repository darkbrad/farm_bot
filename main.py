import logging
import telebot
from button import buttons1,buttons2,buttons3,buttons4
from db import get_connection
import sqlite3
import config
import dbworker
from msg_handler import item_desc,meat_msg

token = '5084341118:AAFHCBMJhqUxDBB2RKrkIPgQODbcnzROIHY'

bot = telebot.TeleBot(token)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
messages=[]
mass=['Адрес доставки',"Имя"]
user_id='1'
user=config.Users(None,None)
items=["Утка","Курица","Гусь"]
order=[]





@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    global user
    user_id=message.chat.id
    user = config.Users(id=user_id, status=config.States.S_START.value)

    bot.send_message(message.chat.id,"Вас привествует FarmBot!", reply_markup=buttons1())
    bot.send_message(message.chat.id,user.status)


def data_input(text):
    return f"Введите {text}"

@bot.message_handler(commands=['reset'])
def cmd_reset(message:telebot.types.Message):
    global mass
    bot.send_message(message.chat.id,f"Данные сброшены.{data_input(mass[0])}")
    global messages
    global user
    with get_connection() as conn:
      dbworker.delete_code(message,conn)
    messages.clear()


    dbworker.set_status(user, config.States.S_ENTER_EMAIL.value)

@bot.message_handler(func=lambda message: dbworker.get_current_status(user) == config.States.S_ENTER_EMAIL.value)
def user_entering_name(message):
    global mass
    global messages
    messages.append(message.text)
    bot.send_message(message.chat.id, f"Введите {mass[1]}")
    global user
    dbworker.set_status(user, config.States.S_ENTER_NAME.value)
@bot.message_handler(func=lambda message: dbworker.get_current_status(user) == config.States.S_ENTER_NAME.value)
def main_rules(message:telebot.types.Message):
    global messages
    global user
    messages.append(message.text)
    with get_connection() as conn:
        dbworker.enter_code(message,messages,conn)


    rules='''Основные правила магазинa:
    1.
    2.
    3.'''



    bot.send_message(message.chat.id, rules,reply_markup=buttons2())
    dbworker.set_status(user,config.States.S_CHOOSE_ITEM.value)
@bot.message_handler(content_types=['text'])
def any_text_message2(message: telebot.types.Message):
    global user
    if message.text=="Связь с человеком":
        bot.send_message(message.chat.id,"Свяжитесь  с нашим адином")
        bot.send_message(message.chat.id,"@fdm195")
    elif message.text=="Присоединиться":
        global mass

        dbworker.set_status(user, config.States.S_ENTER_EMAIL.value)
        bot.send_message(message.chat.id,data_input(mass[0]))

    elif message.text=="Мясо":
        meat_msg(bot,user,message)
    elif message.text=="Назад" :
        if dbworker.compare_status(user,config.States.S_CHOOSE_MEAT.value):
            main_rules(message)
        elif dbworker.compare_status(user,config.States.S_MAKE_ORDER):
            meat_msg(bot,user,message)

    elif message.text=="Изменение личных данных":
        cmd_reset(message)
    elif message.text in items:
        item_desc(message,bot,'fmgjknknkjnbjnfbnxkb',buttons4())
        dbworker.set_status(user,config.States.S_MAKE_ORDER)
    elif message.text.isdigit():
        bot.send_message(message.chat.id,"Заказ оформлен")





if __name__ == "__main__":
    bot.polling(none_stop=True, timeout=123)


