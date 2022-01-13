import logging
import telebot
from button import buttons1,buttons2,buttons3,buttons4,buttons5
from db import get_connection
import sqlite3
import config
import dbworker
from msg_handler import item_desc,meat_msg,get_by_key

token = '5084341118:AAFHCBMJhqUxDBB2RKrkIPgQODbcnzROIHY'

bot = telebot.TeleBot(token)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
messages=[]
mass=['Адрес доставки',"Имя"]
user_id='1'
user=config.Users(None,None)
items=["Утка","Курица","Гусь","Яйца","Молоко"]
item_to_buy=""
order=[]





@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    global user
    user_id=message.chat.id
    user = config.Users(id=user_id, status=config.States.S_START.value)

    bot.send_message(message.chat.id,"Вас привествует FarmBot!", reply_markup=buttons1())


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
    if dbworker.compare_status(user,config.States.S_ENTER_NAME.value):
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
    global item_to_buy
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

        if dbworker.compare_status(user,config.States.S_MAKE_ORDER.value):
            meat_msg(bot,user,message)
        else:main_rules(message)


    elif message.text=="Изменение личных данных":
        cmd_reset(message)
    elif message.text in items:
        item_to_buy=message.text
        with get_connection() as conn:
            line=f'''{item_desc(message,conn)[0]}
Цена:{item_desc(message,conn)[1]}'''
            bot.send_message(message.chat.id, line, reply_markup=buttons4())
        if message.text in ["Яйца","Молоко"]:
            dbworker.set_status(user,config.States.S_MAKE_ORDER_MILK.value)
        elif message.text in ["Утка","Курица","Гусь"]:
            dbworker.set_status(user,config.States.S_MAKE_ORDER.value)

    elif message.text=="Купить":
        line=f"Сколько {get_by_key(item_to_buy)} вы хотите заказать?"
        bot.send_message(message.chat.id,line)
    elif message.text.isdigit() and int(message.text)>0:
        bot.send_message(message.chat.id,"Заказ добавлен в корзину",reply_markup=buttons5())
        with get_connection() as conn:
            dbworker.create_order(message,conn,item_to_buy)
        dbworker.set_status(user,config.States.S_MAKE_ORDER_MILK.value)
    elif message.text=="Оформить и отправить заказ":
        with get_connection() as conn:
            bot.send_message(message.chat.id,"Заказ отправлен.",reply_markup=buttons2())
            line=f'''{dbworker.get_list_items(conn,message)}'''
            bot.send_message(message.chat.id,line)
            dbworker.send_order(message,conn)
            dbworker.clean_cart(conn,message)








if __name__ == "__main__":
    bot.polling(none_stop=True, timeout=123)


