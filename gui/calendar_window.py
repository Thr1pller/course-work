import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox
from datetime import datetime
import json
import os

calendar_file = "calendar_data.json"

# Якщо файл існує — завантажуємо
if os.path.exists(calendar_file):
    with open(calendar_file, "r", encoding="utf-8") as f:
        calendar_events = json.load(f)
else:
    calendar_events = {}

def open_calendar_window():
    root = tk.Tk()
    root.title("Планування приготування")
    root.geometry("420x450")

    cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    # Вибір типу прийому їжі
    tk.Label(root, text="Тип прийому їжі:").pack(pady=(10, 2))

    meal_options = ["Сніданок", "Обід", "Вечеря"]
    meal_var = tk.StringVar(root)
    meal_var.set("Обід")

    meal_menu = tk.OptionMenu(root, meal_var, *meal_options)
    meal_menu.config(width=20)
    meal_menu.pack(pady=5)

    def show_event():
        date = cal.get_date()
        meal = meal_var.get()

        # ОНОВЛЕННЯ: зчитування актуальних даних
        if os.path.exists(calendar_file):
            with open(calendar_file, "r", encoding="utf-8") as f:
                calendar_events = json.load(f)
        else:
            calendar_events = {}

        if date not in calendar_events or meal not in calendar_events[date]:
            messagebox.showinfo("Порожньо", "На цю дату нічого не заплановано.")
            return

        entries = calendar_events[date][meal]
        if not isinstance(entries, list):
            entries = [entries]

        msg = f"📅 {date} — {meal}:\n\n"
        for item in entries:
            if isinstance(item, dict) and "time" in item and "text" in item:
                msg += f"{item['time']}: {item['text']}\n"
            else:
                msg += f"• {item}\n"

        messagebox.showinfo("Заплановане", msg)

    tk.Button(root, text="Переглянути", command=show_event).pack()

    root.mainloop()
