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
        self.root.title("Lista de Tareas – Búsqueda")
        self.tasks = load_tasks()

        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.listbox = tk.Listbox(self.frame, width=60, height=12)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Crear", command=self.create_task).pack(side=tk.LEFT, padx=5)

        # Campo de búsqueda
        search_frame = ttk.Frame(root, padding=(10,0))
        search_frame.pack(fill=tk.X)
        self.search_var = tk.StringVar()
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Ir", command=self.search_tasks).pack(side=tk.LEFT)

        ttk.Button(btn_frame, text="Refrescar", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        self.status = ttk.Label(root, text="")
        self.status.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.refresh_list()

    def refresh_list(self):
        self.tasks = load_tasks()
        self._display_tasks(self.tasks, header=f"Tareas: {len(self.tasks)}")

    def search_tasks(self):
        kw = self.search_var.get().strip().lower()
        if not kw:
            messagebox.showinfo("Buscar", "Ingrese una palabra clave.")
            return
        results = [t for t in self.tasks if kw in t['title'].lower()]
        if not results:
            messagebox.showinfo("Buscar", f"No se encontraron tareas con «{kw}».")
            return
        self._display_tasks(results, header=f"Resultados para «{kw}»: {len(results)}")

    def _display_tasks(self, task_list, header=""):
        self.listbox.delete(0, tk.END)
        for t in task_list:
            estado = "✔" if t['completed'] else "···"
            text = f"{t['id']:<3} {t['title'][:30]:30} {t['due_date']} Prio:{t['priority']} {estado}"
            self.listbox.insert(tk.END, text)
        self.status.config(text=header)

    def create_task(self):
        title = simpledialog.askstring("Título", "Ingrese el título:")
        if not title:
            messagebox.showerror("Error", "Título vacío.")
            return
        due = simpledialog.askstring("Fecha", "Ingrese fecha (YYYY-MM-DD):")
        try: due_date = datetime.strptime(due,'%Y-%m-%d').date().isoformat()
        except: 
            messagebox.showerror("Error", "Fecha inválida."); return
        prio = simpledialog.askinteger("Prioridad", "1 alta,2 media,3 baja:",1,3)
        task = {'id':next_id(self.tasks),'title':title,'due_date':due_date,
                'priority':prio or 2,'completed':False}
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk(); root.geometry("650x450")
    TodoApp(root); root.mainloop()
