import tkinter as tk
from tkinter import ttk
from core.database import connect_to_db
from core.repository import delete_dish, fetch_dishes

def open_delete_dish_window():
    conn = connect_to_db()
    delete_window = tk.Tk()
    delete_window.title("Видалення страви")

    type_var = tk.StringVar(delete_window)
    type_var.set("first_dishes")
    types = ["first_dishes", "second_dishes", "sweets", "drinks"]

    tk.OptionMenu(delete_window, type_var, *types).pack()

    tree = ttk.Treeview(delete_window, columns=("Name", "Time", "Ingredients", "Quantity"))
    tree.heading("#0", text="ID")
    tree.heading("Name", text="Назва")
    tree.heading("Time", text="Час")
    tree.heading("Ingredients", text="Інгредієнти")
    tree.heading("Quantity", text="Кількість")
    tree.pack()

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        dishes = fetch_dishes(conn, type_var.get())
        for dish in dishes:
            tree.insert("", "end", text=dish[0], values=dish[1:])

    def on_delete():
        selected = tree.selection()
        for item in selected:
            dish_id = tree.item(item, "text")
            query = f"DELETE FROM {type_var.get()} WHERE id = %s"
            cursor = conn.cursor()
            cursor.execute(query, (dish_id,))
            conn.commit()
            cursor.close()
        load_data()

    tk.Button(delete_window, text="Завантажити список", command=load_data).pack()
    tk.Button(delete_window, text="Видалити", command=on_delete).pack()

    delete_window.mainloop()
