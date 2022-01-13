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
          "Гусь":"гусей"}
    value=dict.get(key)
    return value
def item_desc(message:telebot.types.Message,bot:telebot.TeleBot,desc:str,reply_markup):
    line=f'''{desc}
    

Сколько {get_by_key(message.text)} вы хотите заказать?'''
    bot.send_message(message.chat.id,line,reply_markup=reply_markup)


def meat_msg(bot,user,message):
    bot.send_message(message.chat.id, "Выберите из предложенных категорий", reply_markup=buttons3())
    dbworker.set_status(user, config.States.S_CHOOSE_MEAT.value)

