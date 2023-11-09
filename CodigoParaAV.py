import sqlite3
from tkinter import *
from tkinter import messagebox
import os

#banco de dados e tabela
def create_database():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY,
        title TEXT,
        status TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Adicionar tarefa
def add_task():
    task_title = entry_task.get()
    task_status = "Pendente"

    if task_title:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO tasks (title, status) VALUES (?,?)
        ''', (task_title, task_status))

        conn.commit()
        conn.close()

        entry_task.delete(0, END)
        get_tasks()

    else:
        messagebox.showerror('Erro', 'Insira uma tarefa')

#tarefas
def get_tasks():
    list_tasks.delete(0, END)

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM tasks
    ''')

    tasks = cursor.fetchall()

    for task in tasks:
        list_tasks.insert(END, f"{task[1]} - {task[2]}")

    conn.close()

# Atualizar tarefa
def update_task():
    selected_task = list_tasks.curselection()
    task_id = selected_task[0] + 1

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE tasks SET status = ? WHERE id = ?
    ''', ('Concluída', task_id))

    conn.commit()
    conn.close()

    get_tasks()

# Excluir tarefa
def delete_task():
    selected_task = list_tasks.curselection()
    task_id = selected_task[0] + 1

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM tasks WHERE id = ?
    ''', (task_id,))

    conn.commit()
    conn.close()

    get_tasks()

# Salvar dados
def save_data():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM tasks
    ''')

    tasks = cursor.fetchall()

    with open('tasks.txt', 'w') as file:
        for task in tasks:
            file.write(f"{task[1]};{task[2]}\n")

    conn.close()

# Carregar dados
def load_data():
    with open('tasks.txt', 'r') as file:
        lines = file.readlines()

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    for line in lines:
        task_title, task_status = line.strip().split(';')

        cursor.execute('''
        INSERT INTO tasks (title, status) VALUES (?,?)
        ''', (task_title, task_status))

    conn.commit()
    conn.close()

    get_tasks()

# Tela principal

def main_screen():
    global window, entry_task, list_tasks, btn_add, btn_update, btn_delete, btn_save, btn_load

    window = Tk()
    window.title('Gerenciador de Tarefas')
    window.geometry('300x300')
    
    entry_task = Entry(window, width=20)
    entry_task.pack(pady=10)

    btn_add = Button(window, text='Adicionar', width=20, command=add_task)
    btn_add.pack(pady=5)

    list_tasks = Listbox(window, width=50, height=15)
    list_tasks.pack(pady=5)

    btn_update = Button(window, text='Atualizar', width=20, command=update_task)
    btn_update.pack(pady=5)

    btn_delete = Button(window, text='Excluir', width=20, command=delete_task)
    btn_delete.pack(pady=5)

    btn_save = Button(window, text='Salvar', width=20, command=save_data)
    btn_save.pack(pady=5)

    btn_load = Button(window, text='Carregar', width=20, command=load_data)
    btn_load.pack(pady=5)

    get_tasks()

    window.mainloop()

create_database()
main_screen()
