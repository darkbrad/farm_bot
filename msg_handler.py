import sqlite3

import dbworker
import config
import telebot
from button import buttons3
def msg_hand(bot,message):
    ...
    # if message.text=="Присоединиться":
    #     global mass
    #     global user
    #     dbworker.set_status(user, config.States.S_ENTER_EMAIL.value)
    #     bot.send_message(message.chat.id,data_input(mass[0]))
    # elif message.text=="Связь с человеком":
    #     bot.send_message(message.chat.id,"Свяжитесь  с нашим адином")
    #     bot.send_message(message.chat.id,"@fdm195")
    # elif message.text=="Мясо":
    #     bot.send_message(message.chat.id,"Выберите из предложенных категорий",reply_markup=buttons3())
    #     dbworker.set_status(user,config.States.S_CHOOSE_MEAT.value)
    # elif message.text=="Назад" and dbworker.compare_status(user,config.States.S_CHOOSE_MEAT.value):
    #     main_rules(message)
    # elif message.text=="Изменение личных данных":
    #     cmd_reset(message)
def get_by_key(key:str):
    dict={"Утка":"уток",
          "Курица":"куриц",
          "Гусь":"гусей",
          "Яйца":"десятков яиц",
        "Молоко":"литров молока"}
    value=dict.get(key)
    return value
def item_desc(message:telebot.types.Message,conn:sqlite3.Connection):
    cur=conn.cursor()
    if type(message)==str:
        cur.execute("SELECT description, price FROM Items WHERE name=?", (message,))
    else:cur.execute("SELECT description, price FROM Items WHERE name=?",(message.text,))
    row=cur.fetchone()
    desc,price=row
    cur.close()
    return desc,price




def meat_msg(bot,users:dict,message):
    bot.send_message(message.chat.id, "Выберите из предложенных категорий", reply_markup=buttons3())
    users[message.chat.id]=config.States.S_CHOOSE_MEAT.value

