import tkinter as tk
from tkinter import ttk
from core.database import connect_to_db
from core.repository import fetch_dishes

def open_show_dishes_window():
    conn = connect_to_db()
    window = tk.Tk()
    window.title("Перегляд страв")
    window.geometry("900x500")

    # Головний контейнер
    window.grid_rowconfigure(2, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Текст + кнопки вгорі
    tk.Label(window, text="Оберіть категорію страв:").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    buttons_frame = tk.Frame(window)
    buttons_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    def load_table(dish_type):
        for row in tree.get_children():
            tree.delete(row)
        dishes = fetch_dishes(conn, dish_type)
        for index, dish in enumerate(dishes, start=1):
            max_len = 80
            name = (dish[1][:max_len] + "…") if len(dish[1]) > max_len else dish[1]
            time = dish[2]
            ingredients = dish[3]
            quantity = dish[4]
            tree.insert("", "end", values=(index, name, time, ingredients, quantity))

    for tname in ["first_dishes", "second_dishes", "sweets", "drinks"]:
        tk.Button(buttons_frame, text=tname, command=lambda dt=tname: load_table(dt)).pack(side="left", padx=5)

    # Область таблиці з прокрутками
    frame = tk.Frame(window)
    frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Time", "Ingredients", "Quantity"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Назва")
    tree.heading("Time", text="Час")
    tree.heading("Ingredients", text="Інгредієнти")
    tree.heading("Quantity", text="Кількість")

    tree.column("ID", width=40, anchor="center")
    tree.column("Name", width=200, anchor="w")
    tree.column("Time", width=100, anchor="center")
    tree.column("Ingredients", width=500, anchor="w")
    tree.column("Quantity", width=80, anchor="center")

    tree.grid(row=0, column=0, sticky="nsew")

    # Скролбари
    y_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    y_scroll.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=y_scroll.set)

    x_scroll = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
    x_scroll.grid(row=3, column=0, sticky="ew")
    tree.configure(xscrollcommand=x_scroll.set)

    def on_row_double_click(event):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0], "values")

            # Пропускаємо індекс
            if len(values) == 5:
                values = values[1:]

            detail_window = tk.Toplevel(window)
            detail_window.title("Деталі рецепта")
            detail_window.geometry("600x400")

            # --- Скролбар + канвас ---
            canvas = tk.Canvas(detail_window)
            scrollbar = tk.Scrollbar(detail_window, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas)

            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # --- Поля ---
            fields = ["Назва", "Час", "Інгредієнти", "Кількість"]

            for i, val in enumerate(values):
                field_name = fields[i] if i < len(fields) else f"Поле {i+1}"
                tk.Label(scroll_frame, text=field_name + ":", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=4)

                text_box = tk.Text(scroll_frame, wrap="word", height=5)
                text_box.insert("1.0", val)
                text_box.config(state="disabled")
                text_box.pack(fill="both", expand=True, padx=10, pady=2)
    
    tree.bind("<Double-1>", on_row_double_click)

    window.mainloop()
