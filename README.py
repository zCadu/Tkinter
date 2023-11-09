import tkinter as tk
import sqlite3
class TaskManager: # criação da classe quer vai gerenciar as tarefas e vai ser responsavel pela lógica do sistema
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_name TEXT,
                        task_description TEXT)''')
        self.conn.commit()

    def add_task(self, task_name, task_description):
        self.c.execute("INSERT INTO tasks (task_name, task_description) VALUES (?, ?)",
                       (task_name, task_description))
        self.conn.commit()

    def get_tasks(self):
        self.c.execute("SELECT * FROM tasks")
        return self.c.fetchall()

    def update_task(self, task_id, task_name, task_description):
        self.c.execute("UPDATE tasks SET task_name=?, task_description=? WHERE id=?",
                       (task_name, task_description, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

        class TaskManagerGUI: # criação da classe responsavel pela interface gráfica
            def __init__(self, root):
                self.root = root
                self.root.title("Sistema de Gerenciamento de Tarefas")

                self.task_manager = TaskManager()

                self.task_name_label = tk.Label(root, text="Nome da Tarefa:")
                self.task_name_label.pack()
                self.task_name_entry = tk.Entry(root)
                self.task_name_entry.pack()

                self.task_description_label = tk.Label(root, text="Descrição da Tarefa:")
                self.task_description_label.pack()
                self.task_description_entry = tk.Entry(root)
                self.task_description_entry.pack()

                self.add_task_button = tk.Button(root, text="Adicionar Tarefa", command=self.add_task)
                self.add_task_button.pack()

                self.tasks_listbox = tk.Listbox(root)
                self.tasks_listbox.pack()

                self.update_task_button = tk.Button(root, text="Atualizar Tarefa", command=self.update_task)
                self.update_task_button.pack()

                self.delete_task_button = tk.Button(root, text="Excluir Tarefa", command=self.delete_task)
                self.delete_task_button.pack()

                self.load_tasks()

            def add_task(self):
                task_name = self.task_name_entry.get()
                task_description = self.task_description_entry.get()
                self.task_manager.add_task(task_name, task_description)
                self.load_tasks()

            def load_tasks(self):
                self.tasks_listbox.delete(0, tk.END)
                tasks = self.task_manager.get_tasks()
                for task in tasks:
                    self.tasks_listbox.insert(tk.END, f"{task[0]} - {task[1]}: {task[2]}")

            def update_task(self):
                selected_task = self.tasks_listbox.curselection()
                if selected_task:
                    task_id = int(self.tasks_listbox.get(selected_task)[0])
                    task_name = self.task_name_entry.get()
                    task_description = self.task_description_entry.get()
                    self.task_manager.update_task(task_id, task_name, task_description)
                    self.load_tasks()

            def delete_task(self):
                selected_task = self.tasks_listbox.curselection()
                if selected_task:
                    task_id = int(self.tasks_listbox.get(selected_task)[0])
                    self.task_manager.delete_task(task_id)
                    self.load_tasks()

        root = tk.Tk()
        app = TaskManagerGUI(root)
        root.mainloop()
