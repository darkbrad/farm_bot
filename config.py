from enum import Enum

class States(Enum):

    S_START = "0"  # Начало нового диалога
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"

class Users():
    def __init__(self,id,status):
        self.id=id
        self.status=status
