import tkinter as tk
from tkinter import ttk
from core.database import connect_to_db
from core.search import search_dishes

def open_search_window():
    conn = connect_to_db()
    search_win = tk.Tk()
    search_win.title("Пошук рецептів")

    table_map = {
        "None": "",
        "First dishes": "first_dishes",
        "Second dishes": "second_dishes",
        "Sweets": "sweets",
        "Drinks": "drinks"
    }
    column_map = {
        "None": "",
        "Name": "name",
        "Ingredients": "ingredients"
    }

    tk.Label(search_win, text="Введіть ключове слово:").pack()
    keyword_entry = tk.Entry(search_win, width=40)
    keyword_entry.pack(pady=5)

    # Таблиці
    tk.Label(search_win, text="Виберіть таблицю (необов'язково):").pack()

    dish_var = tk.StringVar(search_win)
    dish_var.set("None")

    table_options = ["None", "First dishes", "Second dishes", "Sweets", "Drinks"]
    table_menu = tk.OptionMenu(search_win, dish_var, *table_options)
    table_menu.pack(pady=2)
    table_menu.config(width=20)

    # Колонки
    tk.Label(search_win, text="Шукати за (необов'язково):").pack()

    column_var = tk.StringVar(search_win)
    column_var.set("None")

    column_options = ["None", "Name", "Ingredients"]
    column_menu = tk.OptionMenu(search_win, column_var, *column_options)
    column_menu.pack(pady=2)
    column_menu.config(width=20)

    # Таблиця для результатів
    tree = ttk.Treeview(search_win, columns=("Name", "Time", "Ingredients", "Quantity"))
    tree.heading("#0", text="ID")
    tree.heading("Name", text="Назва")
    tree.heading("Time", text="Час")
    tree.heading("Ingredients", text="Інгредієнти")
    tree.heading("Quantity", text="Кількість")
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    def on_search():
        for row in tree.get_children():
            tree.delete(row)

        keyword = keyword_entry.get().strip()
        # Отримуємо внутрішні імена
        selected_table = table_map[dish_var.get()]
        selected_column = column_map[column_var.get()]

        if not keyword:
            return  # якщо немає ключового слова — нічого не робимо

        results = []
        tables = [selected_table] if selected_table else list(table_map.values())[1:]
        for table in tables:
            if selected_column:
                # пошук у вказаній колонці
                results.extend(search_dishes(conn, table, keyword, selected_column))
            else:
                # пошук у name та ingredients
                results.extend(search_dishes(conn, table, keyword, "name"))
                results.extend(search_dishes(conn, table, keyword, "ingredients"))

        unique = {tuple(r) for r in results}
        for row in unique:
            tree.insert("", "end", text=row[0], values=row[1:])

    tk.Button(search_win, text="Пошук", command=on_search).pack(pady=5)

    search_win.mainloop()
