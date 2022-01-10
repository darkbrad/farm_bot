import logging
import telebot



import config
import dbworker

token = '5084341118:AAFHCBMJhqUxDBB2RKrkIPgQODbcnzROIHY'

bot = telebot.TeleBot(token)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
messages=[]
mass=['Адрес доставки',"Имя"]
user_id=''

@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    user_id=message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_1 = telebot.types.KeyboardButton(text="Присоединиться")
    keyboard.add(button_1)
    button_2 = "Связь с человеком"
    keyboard.add(button_2)
    user=config.Users(id=user_id,status=config.States.S_ENTER_NAME.value)
    dbworker.set_status(user, config.States.S_ENTER_NAME.value)
    bot.send_message(message.chat.id,"Вас привествует FarmBot!", reply_markup=keyboard)

user=config.Users(id=user_id,status=config.States.S_ENTER_NAME.value)
print(user.id)
def data_input(text):
    return f"Введите {text}"


@bot.message_handler()
def any_text_message2(message: telebot.types.Message):
    if message.text=="Присоединиться":
        global mass
        bot.send_message(message.chat.id,data_input(mass[0]))

@bot.message_handler(commands=["reset"])
def cmd_reset(message:telebot.types.Message):
    dbworker.set_status(message.chat.id, config.States.S_ENTER_NAME.value)
    bot.send_message(message.chat.id,f"Данные сброшены.{data_input(mass[0])}")
# @dp.message_handler(commands="test1")
# async def cmd_test1(message: types.Message):
#     await message.reply("Test 1")
# @dp.message_handler(func=lambda message: dbworker.get_current_status(user) == config.States.S_ENTER_NAME.value)
# def user_entering_name(message):
#     # В случае с именем не будем ничего проверять, пусть хоть "25671", хоть Евкакий
#     message.answer( "Отличное имя, запомню! Теперь укажи, пожалуйста, свой возраст.")
#     dbworker.set_state(message.chat.id, config.States.S_ENTER_AGE.value)

if __name__ == "__main__":
    # Запуск бота
    bot.polling()


