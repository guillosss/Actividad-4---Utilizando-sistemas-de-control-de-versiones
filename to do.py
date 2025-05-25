import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def next_id(tasks):
    return max((t['id'] for t in tasks), default=0) + 1

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas-Ibero Pruebas de software y aplicabilidad ")
        self.tasks = load_tasks()

        # Layout
        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.frame, width=60, height=15)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Crear", command=self.create_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Marcar/Desmarcar", command=self.toggle_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refrescar", command=self.refresh_list).pack(side=tk.LEFT, padx=5)

        self.status = ttk.Label(root, text="")
        self.status.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.refresh_list()

    def refresh_list(self):
        self.tasks = load_tasks()
        self.listbox.delete(0, tk.END)
        for t in self.tasks:
            status = "✔" if t['completed'] else "···"
            text = f"{t['id']:<3} {t['title'][:30]:30} {t['due_date']} Prio:{t['priority']} {status}"
            self.listbox.insert(tk.END, text)
        self.status.config(text=f"Tareas cargadas: {len(self.tasks)}")

    def on_select(self, event):
        pass

    def create_task(self):
        title = simpledialog.askstring("Título", "Ingrese el título de la tarea:")
        if not title:
            messagebox.showerror("Error", "El título no puede estar vacío.")
            return
        due = simpledialog.askstring("Fecha de vencimiento", "Ingrese la fecha (YYYY-MM-DD):")
        try:
            due_date = datetime.strptime(due, '%Y-%m-%d').date().isoformat()
        except Exception:
            messagebox.showerror("Error", "Formato de fecha inválido.")
            return
        prio = simpledialog.askinteger("Prioridad", "Prioridad (1 alta, 2 media, 3 baja):", minvalue=1, maxvalue=3)
        task = {
            'id': next_id(self.tasks),
            'title': title,
            'due_date': due_date,
            'priority': prio or 2,
            'completed': False
        }
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.refresh_list()

    def edit_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una tarea para editar.")
            return
        idx = sel[0]
        task = self.tasks[idx]
        new_title = simpledialog.askstring("Editar título", "Nuevo título:", initialvalue=task['title'])
        if new_title:
            task['title'] = new_title
        new_due = simpledialog.askstring("Editar fecha", "Nueva fecha (YYYY-MM-DD):", initialvalue=task['due_date'])
        try:
            task['due_date'] = datetime.strptime(new_due, '%Y-%m-%d').date().isoformat()
        except Exception:
            messagebox.showwarning("Formato", "Fecha inválida; se mantiene la anterior.")
        save_tasks(self.tasks)
        self.refresh_list()

    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una tarea para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar la tarea seleccionada?"):
            idx = sel[0]
            del self.tasks[idx]
            save_tasks(self.tasks)
            self.refresh_list()

    def toggle_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una tarea para marcar/desmarcar.")
            return
        idx = sel[0]
        self.tasks[idx]['completed'] = not self.tasks[idx]['completed']
        save_tasks(self.tasks)
        self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x450")
    app = TodoApp(root)
    root.mainloop()
