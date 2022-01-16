import logging
import telebot

import msg_handler
from button import buttons1,buttons2,buttons3,buttons4,buttons5
from db import get_connection
import config
import dbworker
from msg_handler import item_desc,meat_msg,get_by_key

token = '5084341118:AAFHCBMJhqUxDBB2RKrkIPgQODbcnzROIHY'

bot = telebot.TeleBot(token)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
messages={}
user_id='1'
items=["Утка","Курица","Гусь","Яйца","Молоко"]
users={}
item_to_buy=""
order=[]
order_list={}




@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    global users
    user_id=message.chat.id
    if "148" in users.values():
        users.clear()
    users.update({message.chat.id:config.States.S_START.value})

    with get_connection() as conn:
        if dbworker.in_db(message,conn):
            bot.send_message(message.chat.id, "Вас привествует FarmBot!")
            bot.send_message(message.chat.id, "Введите адресс доставки ")
            users[user_id]=config.States.S_ENTER_EMAIL.value
        else:
            bot.send_message(message.chat.id, "Вас привествует FarmBot!",reply_markup=buttons1())
            users[user_id]=config.States.S_ENTER_NAME.value

@bot.message_handler(commands=['reset'])
def cmd_reset(message:telebot.types.Message):
    global mass
    bot.send_message(message.chat.id,f"Данные сброшены.Введите адресс доставки")
    global messages
    with get_connection() as conn:
      dbworker.delete_code(message,conn)
    messages.clear()


    users[message.chat.id]=config.States.S_ENTER_EMAIL.value

@bot.message_handler(func=lambda message: msg_handler.compare(users,message,config.States.S_ENTER_EMAIL.value))
def user_entering_name(message):
    global messages
    global users
    global user_id

    bot.send_message(message.chat.id, "Введите имя")
    messages.update({message.text: message.chat.id})
    users[message.chat.id]=config.States.S_ENTER_NAME.value

@bot.message_handler(func=lambda message: msg_handler.compare(users,message,config.States.S_ENTER_NAME.value))
def main_rules(message:telebot.types.Message):
    global messages
    global users
    with get_connection() as conn:
        if users[message.chat.id]==config.States.S_ENTER_NAME.value and dbworker.in_db(message,conn):
            messages.update({message.text: message.chat.id})
            dbworker.enter_code(message,messages,conn)


    rules='''Основные правила магазинa:
    1.
    2.
    3.'''



    bot.send_message(message.chat.id, rules,reply_markup=buttons2())
    users[message.chat.id]=config.States.S_CHOOSE_ITEM.value
@bot.message_handler(content_types=['text'])
def any_text_message2(message: telebot.types.Message):
    global users
    global order_list
    global user_id
    if message.text=="Связь с человеком":
        bot.send_message(message.chat.id,"Свяжитесь  с нашим адином")
        bot.send_message(message.chat.id,"@fdm195")

    elif message.text=="Мясо":
        meat_msg(bot,users,message)
    elif message.text=="Назад" :

        if users[message.chat.id]==config.States.S_MAKE_ORDER.value:
            meat_msg(bot,users,message)
        else:main_rules(message)


    elif message.text=="Изменение личных данных":
        cmd_reset(message)
    elif message.text in items:
        item_to_buy=message.text
        order_list.update({message.chat.id:item_to_buy})


        with get_connection() as conn:
            line=f'''{item_desc(message.text,conn)[0]}
Цена:{item_desc(message.text,conn)[1]}'''
            bot.send_message(message.chat.id, line, reply_markup=buttons4())
        if message.text in ["Яйца","Молоко"]:
            users[message.chat.id] =config.States.S_MAKE_ORDER_MILK.value
        elif message.text in ["Утка","Курица","Гусь"]:
            users[message.chat.id]=config.States.S_MAKE_ORDER.value

    elif message.text=="Купить":
        line=f"Сколько {get_by_key(order_list.get(message.chat.id))} вы хотите заказать?"
        bot.send_message(message.chat.id,line)
    elif message.text.isdigit() and int(message.text)>0:
        bot.send_message(message.chat.id,"Заказ добавлен в корзину",reply_markup=buttons5())
        with get_connection() as conn:
            dbworker.create_order(message,conn,order_list.get(message.chat.id))
        users[message.chat.id]=config.States.S_MAKE_ORDER_MILK.value
    elif message.text=="Оформить и отправить заказ":
        with get_connection() as conn:
            bot.send_message(message.chat.id,"Заказ отправлен.",reply_markup=buttons2())
            line=f'''{dbworker.get_list_items(conn,message)}
К оплате:{dbworker.get_cost(conn,message)}'''
            bot.send_message(message.chat.id,line)
            dbworker.send_order(message,conn)
            dbworker.clean_cart(conn,message)
            line=f'''Покупатель:{dbworker.get_adress_get_name(conn,message)[1]} 
По адрессу {dbworker.get_adress_get_name(conn,message)[0]}
Товары для доставки: {dbworker.get_list_items(conn,message)}
Стоимость:{dbworker.get_cost(conn,message)}'''
            bot.send_message(97702779,line)








if __name__ == "__main__":
    bot.polling(none_stop=True, timeout=123)


