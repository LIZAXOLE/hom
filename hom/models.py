USERS = [
    {"login": "admin", "password": "admin", "role": "Администратор",
    "full_name": "Администратор Системы", "locked": False},
    {"login": "ivanov", "password": "1234", "role": "Пользователь",
    "full_name": "Иванов Иван", "locked": True},
    {"login": "petrov", "password": "qwerty", "role": "Пользователь",
    "full_name": "Петров Пётр", "locked": False },
]

def find_user(login, password):
    for u in USERS:
        if u["login"] == login and u["password"] == password:
            return u
    return None
