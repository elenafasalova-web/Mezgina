import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

# Глобальные переменные
records = []

def load_records():
    global records
    try:
        with open('records.json', 'r', encoding='utf-8') as f:
            records = json.load(f)
    except FileNotFoundError:
        records = []

def save_records():
    with open('records.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=4, ensure_ascii=False)

def add_record():
    date_str = entry_date.get().strip()
    temp_str = entry_temp.get().strip()
    description = entry_desc.get().strip()
    precip = var_precip.get()

    # Проверка корректности данных
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ГГГГ-ММ-ДД.")
        return

    try:
        temperature = float(temp_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Температура должна быть числом.")
        return

    if not description:
        messagebox.showerror("Ошибка", "Описание не должно быть пустым.")
        return

    record = {
        'date': date_str,
        'temperature': temperature,
        'description': description,
        'precipitation': precip
    }
    records.append(record)
    update_table()
    clear_entries()

def update_table(filtered_records=None):
    for row in tree.get_children():
        tree.delete(row)
    display_records = filtered_records if filtered_records is not None else records
    for rec in display_records:
        tree.insert('', tk.END, values=(
            rec['date'],
            rec['temperature'],
            rec['description'],
            'Да' if rec['precipitation'] else 'Нет'
        ))

def clear_entries():
    entry_date.delete(0, tk.END)
    entry_temp.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    var_precip.set(False)

def filter_by_date():
    date_str = entry_date_filter.get().strip()
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ГГГГ-ММ-ДД.")
        return
    filtered = [r for r in records if r['date'] == date_str]
    update_table(filtered)

def filter_by_temp():
    try:
        threshold = float(entry_temp_filter.get().strip())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите число для температуры.")
        return
    filtered = [r for r in records if r['temperature'] > threshold]
    update_table(filtered)

def show_all():
    update_table()

def save_to_file():
    save_records()
    messagebox.showinfo("Сохранено", "Данные успешно сохранены.")

def load_from_file():
    load_records()
    update_table()

# Создаем окно и компоненты
root = tk.Tk()
root.title("Weather Diary")

# Ввод данных
tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_date = tk.Entry(root)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Температура:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_temp = tk.Entry(root)
entry_temp.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_desc = tk.Entry(root)
entry_desc.grid(row=2, column=1, padx=5, pady=5)

var_precip = tk.BooleanVar()
cb_precip = tk.Checkbutton(root, text='Осадки', variable=var_precip)
cb_precip.grid(row=3, column=1, padx=5, pady=5, sticky='w')

btn_add = tk.Button(root, text="Добавить запись", command=add_record)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# Таблица
columns = ('date', 'temperature', 'description', 'precipitation')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.title())
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Фильтрация
tk.Label(root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=6, column=0, padx=5, pady=5, sticky='e')
entry_date_filter = tk.Entry(root)
entry_date_filter.grid(row=6, column=1, padx=5, pady=5)

btn_filter_date = tk.Button(root, text="Фильтровать по дате", command=filter_by_date)
btn_filter_date.grid(row=7, column=0, pady=5)

tk.Label(root, text="Фильтр по температуре (<):").grid(row=6, column=2, padx=5, pady=5, sticky='e')
entry_temp_filter = tk.Entry(root)
entry_temp_filter.grid(row=6, column=3, padx=5, pady=5)

btn_filter_temp = tk.Button(root, text="Фильтровать по температуре", command=filter_by_temp)
btn_filter_temp.grid(row=7, column=2, pady=5)

btn_show_all = tk.Button(root, text="Показать все", command=show_all)
btn_show_all.grid(row=7, column=3, pady=5)

# Меню для сохранения/загрузки
btn_save = tk.Button(root, text="Сохранить в файл", command=save_to_file)
btn_save.grid(row=8, column=0, pady=10)

btn_load = tk.Button(root, text="Загрузить из файла", command=load_from_file)
btn_load.grid(row=8, column=1, pady=10)

# Загрузка данных при старте
load_records()
update_table()

root.mainloop()
