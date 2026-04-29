import tkinter as tk
from tkinter import messagebox as mb, ttk
import random, json, os

# Данные автора и проекта
AUTHOR = "Ваше Имя"
GIT_HUB = "https://github.com/dasazabina3@gmail.com/ваш_fish"
FILE = "history.json"

# База задач
TASK_POOL = {
    "Учёба": ["Повторить синтаксис Python", "Прочитать 10 страниц книги", "Решить задачу на LeetCode", "Посмотреть лекцию на YouTube"],
    "Спорт": ["Сделать 20 приседаний", "Планка 1.5 минуты", "Прогулка быстрым шагом", "Растяжка всего тела", "15 отжиманий"],
    "Работа": ["Разобрать входящую почту", "Обновить список дел", "Проверить уведомления в мессенджерах", "Навести порядок на столе"]
}

history = []

def save_data():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def load_data():
    global history
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            history = json.load(f)

def update_view(filter_cat="Все"):
    listbox.delete(0, tk.END)
    for item in reversed(history):
        if filter_cat == "Все" or item["type"] == filter_cat:
            listbox.insert(tk.END, f"[{item['type']}] {item['task']}")

def add_task(text, cat):
    if not text.strip():
        return mb.showwarning("Внимание", "Задача не может быть пустой!")
    history.append({"task": text, "type": cat})
    save_data()
    update_view(filter_combo.get())

def on_generate():
    cat = gen_combo.get()
    target_cat = random.choice(list(TASK_POOL.keys())) if cat == "Любая" else cat
    task = random.choice(TASK_POOL[target_cat])
    lbl_res.config(text=f"Сгенерировано: {task}")
    add_task(task, target_cat)

def on_clear():
    if mb.askyesno("Очистка", "Удалить всю историю?"):
        history.clear()
        save_data()
        update_view()

# Настройка GUI
root = tk.Tk()
root.title(f"Random Task Generator | {AUTHOR}")
root.geometry("450x600")

# Блок генерации
tk.Label(root, text="Генератор задач", font=("Arial", 14, "bold")).pack(pady=10)
gen_frame = tk.Frame(root)
gen_frame.pack(pady=5)

gen_combo = ttk.Combobox(gen_frame, values=["Любая"] + list(TASK_POOL.keys()), state="readonly", width=12)
gen_combo.current(0)
gen_combo.pack(side="left", padx=5)

tk.Button(gen_frame, text="Создать", command=on_generate, bg="#4caf50", fg="white").pack(side="left")
lbl_res = tk.Label(root, text="Нажмите 'Создать'", fg="grey", wraplength=350)
lbl_res.pack(pady=10)

# Блок ручного ввода
add_frame = tk.LabelFrame(root, text=" Своя задача ", padx=10, pady=10)
add_frame.pack(fill="x", padx=20)

ent_task = tk.Entry(add_frame, width=25)
ent_task.pack(side="left", padx=5)
cat_combo = ttk.Combobox(add_frame, values=list(TASK_POOL.keys()), state="readonly", width=10)
cat_combo.current(0)
cat_combo.pack(side="left", padx=5)
tk.Button(add_frame, text="+", command=lambda: [add_task(ent_task.get(), cat_combo.get()), ent_task.delete(0, tk.END)]).pack(side="left")

# Блок истории
tk.Label(root, text="История задач", font=("Arial", 10, "bold")).pack(pady=(15, 5))
filter_combo = ttk.Combobox(root, values=["Все", "Учёба", "Спорт", "Работа"], state="readonly")
filter_combo.current(0)
filter_combo.pack(pady=5)
filter_combo.bind("<<ComboboxSelected>>", lambda e: update_view(filter_combo.get()))

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=5, padx=20)

tk.Button(root, text="Очистить историю", command=on_clear, fg="red", relief="flat").pack()

# Запуск
load_data()
update_view()
root.mainloop()