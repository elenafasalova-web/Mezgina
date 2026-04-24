import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []

        # Поля ввода
        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0)
        self.temp_entry = tk.Entry(root)
        self.temp_entry.grid(row=1, column=1)

        tk.Label(root, text="Описание:").grid(row=2, column=0)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=2, column=1)

        self.rain_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Осадки", variable=self.rain_var).grid(row=3, column=0, columnspan=2)

        # Кнопка добавления
        tk.Button(root, text="Добавить запись", command=self.add_record).grid(row=4, column=0, columnspan=2)

        # Таблица записей
        self.tree = ttk.Treeview(root, columns=("date", "temp", "desc", "rain"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Температура")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("rain", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=2)

        # Фильтрация по дате
        tk.Label(root, text="Фильтр по дате:").grid(row=6, column=0)
        self.filter_date_entry = tk.Entry(root)
        self.filter_date_entry.grid(row=6, column=1)
        tk.Button(root, text="Фильтровать по дате", command=self.filter_by_date).grid(row=7, column=0, columnspan=2)

        # Фильтрация по температуре
        tk.Label(root, text="Фильтр по температуре (>):").grid(row=8, column=0)
        self.filter_temp_entry = tk.Entry(root)
        self.filter_temp_entry.grid(row=8, column=1)
        tk.Button(root, text="Фильтровать по температуре", command=self.filter_by_temp).grid(row=9, column=0, columnspan=2)

        # Сохранение/загрузка
        tk.Button(root, text="Сохранить в JSON", command=self.save_to_json).grid(row=10, column=0)
        tk.Button(root, text="Загрузить из JSON", command=self.load_from_json).grid(row=10, column=1)
def add_record(self):
    date = self.date_entry.get()
    temp = self.temp_entry.get()
    desc = self.desc_entry.get()
    rain = self.rain_var.get()

    # Валидация
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат даты (ГГГГ-ММ-ДД)")
        return

    try:
        temp = float(temp)
    except ValueError:
        messagebox.showerror("Ошибка", "Температура должна быть числом")
        return

    if not desc:
        messagebox.showerror("Ошибка", "Описание не может быть пустым")
        return

    # Добавление в список и таблицу
    record = {"date": date, "temp": temp, "desc": desc, "rain": rain}
    self.records.append(record)
    self.tree.insert("", "end", values=(date, temp, desc, "Да" if rain else "Нет"))
def filter_by_date(self):
    filter_date = self.filter_date_entry.get()
    for item in self.tree.get_children():
        self.tree.delete(item)
    for record in self.records:
        if record["date"] == filter_date:
            self.tree.insert("", "end", values=(record["date"], record["temp"], record["desc"], "Да" if record["rain"] else "Нет"))
def filter_by_date(self):
    filter_date = self.filter_date_entry.get()
    for item in self.tree.get_children():
        self.tree.delete(item)
    for record in self.records:
        if record["date"] == filter_date:
            self.tree.insert("", "end", values=(record["date"], record["temp"], record["desc"], "Да" if record["rain"] else "Нет"))
def save_to_json(self):
    filename = "weather_diary.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(self.records, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Успех", f"Данные сохранены в {filename}")
def load_from_json(self):
    filename = "weather_diary.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            self.records = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл {filename} не найден")
        return

    # Очистка таблицы и загрузка данных
    for item in self.tree.get_children():
        self.tree.delete(item)
    for record in self.records:
        self.tree.insert("", "end", values=(record["date"], record["temp"], record["desc"], "Да" if record["rain"] else "Нет"))
