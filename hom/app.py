import os
import random
import tkinter as tk
from tkinter import messagebox, ttk

from models import * 

CURRENT_USER = None
ENTRY_LOGIN = None

BG = "#f9f1e5"
FIELD_BG = "#ffffff"
FIELD_FG = "#22262b"

FONT_TITLE = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 11, "bold")
FONT_BUTTON = ("Arial", 12, "bold")

root = tk.Tk()
root.title("Учебное приложение")
root.geometry("720x640")
root.configure(bg=BG)

container = tk.Frame(root, bg=BG)
container.pack(fill="both", expand=True, padx=20, pady=20)

def clear_screen():
    for w in container.winfo_children():
        w.destroy()

def make_title(text):
    return tk.Label(container, text=text, bg=BG, fg=FIELD_FG, font=FONT_TITLE)

def make_label(text):
    return tk.Label(container, text=text, bg=BG, fg=FIELD_FG,
                    font=FONT_LABEL, anchor="w")

def make_entry(password=False):
    entry = tk.Entry(container, font=FONT_BUTTON, bg=FIELD_BG, fg=FIELD_FG,
                     insertbackground=FIELD_FG, relief="solid", borderwidth=1)
    if password:
        entry.configure(show="*")
    return entry

def make_button(text, command, parent=None):
    host = container if parent is None else parent
    return tk.Button(host, text=text, command=command, font=FONT_BUTTON)

def try_login(login, password):
    global CURRENT_USER
    login = login.strip()
    password = password.strip()
    if not login or not password:
        messagebox.showwarning("Внимание", "Заполните логин и пароль.")
        return
    user = find_user(login, password)
    if user is None:
        messagebox.showerror("Ошибка входа","Вы ввели неверный логин или пароль.""Пожалуйста проверьте ещё раз введенные данные")
        return
    if user["locked"]:
        messagebox.showerror("Блокировка","Вы заблокированы. Обратитесь к администратору")
        return
    CURRENT_USER = user
    messagebox.showinfo("Авторизация", "Вы успешно авторизовались")
    if user["role"] == "Администратор":
        open_admin()
    else:
        open_user()

def open_login():
    global ENTRY_LOGIN
    clear_screen()
    make_title("Вход в систему").pack(pady=(0, 10))

    make_label("Логин").pack(fill="x")
    ENTRY_LOGIN = make_entry()
    ENTRY_LOGIN.pack(fill="x", pady=(0, 8))

    make_label("Пароль").pack(fill="x")
    entry_pass = make_entry(password=True)
    entry_pass.pack(fill="x", pady=(0, 4))

    make_button("Войти",
                lambda: try_login(ENTRY_LOGIN.get(), entry_pass.get())
                ).pack(fill="x", ipady=6)

def open_user():
    clear_screen()
    make_title("Рабочее место пользователя").pack(pady=(0, 10))
    make_label(f"Вы вошли как: {CURRENT_USER['login']}").pack(fill="x", pady=(0, 6))
    make_label(f"Роль: {CURRENT_USER['role']}").pack(fill="x", pady=(0, 20))
    make_button("Выйти", open_login).pack(ipadx=24, ipady=4)

def open_edit_user():
    clear_screen()
    make_title("Изменение пользователя").pack(pady=(0, 10))

    make_label("ФИО").pack(fill="x")
    e_name = make_entry()
    e_name.pack(fill="x", pady=(0, 8))

    make_label("Пароль").pack(fill="x")
    e_pass = make_entry()
    e_pass.pack(fill="x", pady=(0, 8))

    make_label("Роль").pack(fill="x")
    combo_role = ttk.Combobox(container, values=["Пользователь", "Администратор"],
                              state="readonly", font=FONT_BUTTON)
    combo_role.pack(fill="x", pady=(0, 10))

    row = tk.Frame(container, bg=BG)
    row.pack(fill="x")
    make_button("Сохранить",open_admin, parent=row).pack(side="left", padx=(0, 6))
    make_button("Разблокировать", parent=row).pack(side="left", padx=(0, 6))
    make_button("Удалить", parent=row).pack(side="left", padx=(0, 6))
    make_button("Отмена", open_admin, parent=row).pack(side="right")

def open_admin():
    clear_screen()
    make_title("Панель администратора").pack(pady=(0, 5))
    make_label(f"Вы вошли как: {CURRENT_USER['login']}").pack(fill="x", pady=(0, 10))

    tree = ttk.Treeview(container,
                        columns=("login", "full_name", "role", "locked"),
                        show="headings", height=8)
    tree.heading("login", text="Логин")
    tree.heading("full_name", text="ФИО")
    tree.heading("role", text="Роль")
    tree.heading("locked", text="Заблокирован")
    tree.column("login", width=120, anchor="w")
    tree.column("full_name", width=180, anchor="w")
    tree.column("role", width=130, anchor="w")
    tree.column("locked", width=110, anchor="center")

    row = tk.Frame(container, bg=BG)
    row.pack(fill="x")
    make_button("Добавить", open_add_user, parent=row).pack(side="left", padx=(0, 6))
    make_button("Изменить", open_edit_user, parent=row).pack(side="left", padx=(0, 6))
    make_button("Выйти", open_login, parent=row).pack(side="right")

def save_user(login, password, role, full_name):
    open_admin()

def open_add_user():
    clear_screen()
    make_title("Новый пользователь").pack(pady=(0, 15))
    make_label("Логин").pack(fill="x")
    e_login = make_entry()
    e_login.pack(fill="x", pady=(0, 10))
    make_label("ФИО").pack(fill="x")
    e_name = make_entry()
    e_name.pack(fill="x", pady=(0, 10))
    make_label("Пароль").pack(fill="x")
    e_pass = make_entry()
    e_pass.pack(fill="x", pady=(0, 10))
    make_button("Сохранить")
    make_button("Отмена", open_admin).pack(fill="x", pady=(8, 0), ipady=4)

open_login()
root.mainloop()