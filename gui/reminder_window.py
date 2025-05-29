import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import json, os, datetime, threading

calendar_file = "calendar_data.json"

def open_reminder_window():
    root = tk.Tk()
    root.title("Нагадування")
    root.geometry("400x500")

    # Календар
    tk.Label(root, text="Оберіть дату:").pack()
    cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=5)

    # Вибір часу
    tk.Label(root, text="Оберіть час (год:хв):").pack()
    time_frame = tk.Frame(root)
    time_frame.pack()

    hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=5, format="%02.0f")
    hour_spinbox.pack(side="left", padx=2)
    hour_spinbox.delete(0, "end")
    hour_spinbox.insert(0, "12")

    tk.Label(time_frame, text=":").pack(side="left")

    minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=5, format="%02.0f")
    minute_spinbox.pack(side="left", padx=2)
    minute_spinbox.delete(0, "end")
    minute_spinbox.insert(0, "0")

    # Тип прийому їжі
    tk.Label(root, text="Тип прийому їжі:").pack(pady=(10, 2))
    meal_var = tk.StringVar(root)
    meal_var.set("Обід")
    meal_options = ["Сніданок", "Обід", "Вечеря"]
    tk.OptionMenu(root, meal_var, *meal_options).pack()

    # Повідомлення
    tk.Label(root, text="Що показати в нагадуванні:").pack()
    msg_entry = tk.Entry(root, width=40)
    msg_entry.pack(pady=5)

    def send_later():
        date = cal.get_date()
        hour = int(hour_spinbox.get())
        minute = int(minute_spinbox.get())
        meal = meal_var.get()
        message = msg_entry.get().strip()

        if not message:
            if os.path.exists(calendar_file):
                with open(calendar_file, "r", encoding="utf-8") as f:
                    events = json.load(f)
                meals = events.get(date, {}).get(meal, [])
                message = "\n".join(meals) if meals else "Нічого не заплановано"
            else:
                message = "Нічого не заплановано"

        # Розрахунок різниці в секундах
        target = datetime.datetime.strptime(f"{date} {hour:02d}:{minute:02d}", "%Y-%m-%d %H:%M")
        now = datetime.datetime.now()
        delta = (target - now).total_seconds()

        if delta <= 0:
            messagebox.showerror("Помилка", "Оберіть час у майбутньому!")
            return

        def show_notification():
            messagebox.showinfo("Нагадування", message)

        timer = threading.Timer(delta, show_notification)
        timer.daemon = True
        timer.start()

        # Запис у calendar_data.json
        if os.path.exists(calendar_file):
            with open(calendar_file, "r", encoding="utf-8") as f:
                calendar_events = json.load(f)
        else:
            calendar_events = {}

        # Ініціалізація структури
        if date not in calendar_events:
            calendar_events[date] = {}
        if meal not in calendar_events[date]:
            calendar_events[date][meal] = []

        calendar_events[date][meal].append(message)

        # Збереження у файл
        with open(calendar_file, "w", encoding="utf-8") as f:
            json.dump(calendar_events, f, indent=2, ensure_ascii=False)

        messagebox.showinfo("Готово", f"Нагадування встановлено на {date} о {hour:02d}:{minute:02d}")

    tk.Button(root, text="Установити нагадування", command=send_later).pack(pady=10)

    root.mainloop()
