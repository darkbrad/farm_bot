import config
from config import Users
import sqlite3
import telebot


def get_current_status(user:Users):
    return user.status

def set_status(user:Users,status:str):
    user.status=status
    return user
def compare_status(user:Users,status):
    return user.status==status

def enter_code(message:telebot.types.Message,messages:list,conn:sqlite3.Connection):
    cur=conn.cursor()

    id = int(message.chat.id)
    name = messages[1]
    adress = messages[0]
    cur.execute(f"INSERT  INTO Users (id,name,adress) VALUES (?,?,?)",(id,name,adress))


    cur.close()
def delete_code(message:telebot.types.Message,conn:sqlite3.Connection):
    cur=conn.cursor()
    id=message.chat.id
    cur.execute(f"DELETE FROM Users WHERE id=?",(id,))
    cur.close()