import tkinter as tk
from gui.add_dish_window import open_add_dish_window
from gui.show_dishes_window import open_show_dishes_window
from gui.delete_dish_window import open_delete_dish_window
from gui.search_window import open_search_window
from gui.ai_window import open_ai_window
from gui.calendar_window import open_calendar_window
from gui.reminder_window import open_reminder_window

def show_main_menu():
    root = tk.Tk()
    root.title("Меню")
    root.geometry("400x500")
    root.resizable(True, True)

    buttons = [
        ("Додати рецепт", open_add_dish_window),
        ("Показати рецепти", open_show_dishes_window),
        ("Видалити рецепт", open_delete_dish_window),
        ("Пошук рецептів", open_search_window),
        ("AI-помічник", open_ai_window),
        ("Календар", open_calendar_window),
        ("Нагадування", open_reminder_window),
        ("Вийти", root.destroy)
    ]

    for text, command in buttons:
        tk.Button(root, text=text, command=command, width=25).pack(pady=6)

    root.mainloop()
