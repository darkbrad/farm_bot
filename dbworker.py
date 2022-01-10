from config import Users
def get_current_status(user:Users):
    return user.status

def set_status(user:Users,status:str):
    user.status=status
    return user

    return user