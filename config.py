from enum import Enum
from typing import Optional

class States(Enum):

    S_START = "0"  # Начало нового диалога
    S_ENTER_EMAIL = "1"
    S_ENTER_NAME = "2"
    S_CHOOSE_ITEM="3"
    S_CHOOSE_MEAT="4"
    S_MAKE_ORDER="5"
    S_MAKE_ORDER_MILK="6"

class Users():
    def __init__(self,id:Optional[int],status:Optional[int]):
        self.id=id
        self.status=status


