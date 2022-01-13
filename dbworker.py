import config
from config import Users
import sqlite3
import telebot
from msg_handler import item_desc


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
def create_order(message:telebot.types.Message,conn:sqlite3.Connection,item:str):
    cur=conn.cursor()
    byer_id=message.chat.id
    cost=(item_desc(item,conn)[1])
    cur.execute(f"INSERT INTO Cart (byer_id,item,cost,amount) VALUES (?,?,?,?)",(byer_id,item,cost,message.text))
    cur.close()

def get_cost(conn:sqlite3.Connection,message:telebot.types.Message):
    cur = conn.cursor()
    b=0

    cur.execute(f"SELECT Cart.cost,Cart.amount FROM Cart WHERE byer_id=?",(message.chat.id,))
    data=cur.fetchall()
    for i in data:
        x=i[0]
        y=i[1]
        b=b+x*y
    cur.close()
    return b

def get_list_items(conn:sqlite3.Connection,message:telebot.types.Message):
    cur=conn.cursor()
    cur.execute(f"SELECT Cart.item,Cart.amount FROM Cart WHERE byer_id=?",(message.chat.id,))
    data=cur.fetchall()
    s=""
    for i in data:
        items=i[0]+"-"+str(i[1])+","
        s=s+items
    s=s[:len(s)-1]
    cur.close()
    return s
def send_order(message:telebot.types.Message,conn:sqlite3.Connection):
    cur=conn.cursor()
    byer_id = message.chat.id
    cost=get_cost(conn,message)
    items=get_list_items(conn,message)

    cur.execute(f"INSERT INTO Orders (byer_id,cost,items) VALUES (?,?,?)",(byer_id,cost,items))
    cur.close()
def clean_cart(conn:sqlite3.Connection,message:telebot.types.Message):
    cur=conn.cursor()
    cur.execute("DELETE FROM Cart WHERE byer_id=?",(message.chat.id,))
    cur.close()
