import tkinter as tk
from core.database import connect_to_db
from core.repository import insert_dish

def open_add_dish_window():
    conn = connect_to_db()

    def on_add():
        dish_type = type_var.get()
        name = name_entry.get()
        time_cooking = time_entry.get()
        ingredients = ingredients_entry.get()
        quantity = quantity_entry.get()

        insert_dish(conn, dish_type, name, time_cooking, ingredients, quantity)
        add_window.destroy()

    add_window = tk.Tk()
    add_window.title("Додати нову страву")
    add_window.geometry("400x400")
    add_window.resizable(True, True)

    # Тип страви
    tk.Label(add_window, text="Тип страви:").pack(pady=(10, 2))
    type_var = tk.StringVar(add_window, value="first_dishes")
    type_options = ["first_dishes", "second_dishes", "sweets", "drinks"]
    type_menu = tk.OptionMenu(add_window, type_var, *type_options)
    type_menu.config(width=30)
    type_menu.pack(pady=5)

    # Назва
    tk.Label(add_window, text="Назва:").pack()
    name_entry = tk.Entry(add_window, width=40)
    name_entry.pack(pady=5)

    # Час
    tk.Label(add_window, text="Час приготування:").pack()
    time_entry = tk.Entry(add_window, width=40)
    time_entry.pack(pady=5)

    # Інгредієнти
    tk.Label(add_window, text="Інгредієнти:").pack()
    ingredients_entry = tk.Entry(add_window, width=40)
    ingredients_entry.pack(pady=5)

    # Кількість
    tk.Label(add_window, text="Кількість:").pack()
    quantity_entry = tk.Entry(add_window, width=40)
    quantity_entry.pack(pady=5)

    # Кнопка
    tk.Button(add_window, text="Додати", command=on_add, width=20).pack(pady=15)

    add_window.mainloop()
