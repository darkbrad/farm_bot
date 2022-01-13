import telebot
def buttons1():
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_1 = telebot.types.KeyboardButton(text="Присоединиться")
    keyboard.add(button_1)
    button_2 = telebot.types.KeyboardButton(text="Связь с человеком")
    keyboard.add(button_2)
    return keyboard
def buttons2():
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

    button_1 = telebot.types.KeyboardButton(text="Мясо")

    button_2 = telebot.types.KeyboardButton(text="Яйца")

    button_3 = telebot.types.KeyboardButton(text="Молоко")

    button_4 = telebot.types.KeyboardButton(text="Связь с человеком")

    button_5 = telebot.types.KeyboardButton(text="Правила")

    button_6 = telebot.types.KeyboardButton(text="Изменение личных данных")
    keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6)
    return keyboard

def buttons3():
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

    button_1 = telebot.types.KeyboardButton(text="Утка")

    button_2 = telebot.types.KeyboardButton(text="Курица")

    button_3 = telebot.types.KeyboardButton(text="Гусь")

    button_4 = telebot.types.KeyboardButton(text="Связь с человеком")

    button_5 = telebot.types.KeyboardButton(text="Назад")

    keyboard.add(button_1, button_2, button_3, button_4, button_5)
    return keyboard

def buttons4():
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

    button_1 = telebot.types.KeyboardButton(text="Купить")

    button_4 = telebot.types.KeyboardButton(text="Связь с человеком")

    button_5 = telebot.types.KeyboardButton(text="Назад")

    keyboard.add(button_1, button_4, button_5)
    return keyboard
def buttons5():
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

    button_1 = telebot.types.KeyboardButton(text="Мясо")

    button_2 = telebot.types.KeyboardButton(text="Яйца")

    button_3 = telebot.types.KeyboardButton(text="Молоко")

    button_4 = telebot.types.KeyboardButton(text="Связь с человеком")

    button_5 = telebot.types.KeyboardButton(text="Правила")

    button_6 = telebot.types.KeyboardButton(text="Изменение личных данных")

    button_6 = telebot.types.KeyboardButton(text="Оформить и отправить заказ")
    keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6)
    return keyboard