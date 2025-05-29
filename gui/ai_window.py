import tkinter as tk
from tkinter import ttk, messagebox
from ai.assistant import ask_ai
from core.database import connect_to_db
from core.repository import insert_dish
import re

def open_ai_window():
    window = tk.Tk()
    window.title("AI-помічник з рецептами")
    window.geometry("900x600")
    window.resizable(True, True)

    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Поле для запиту
    tk.Label(window, text="Введіть запит до AI:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    prompt_entry = tk.Text(window, height=4, wrap="word")
    prompt_entry.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    # Поле для відповіді
    tk.Label(window, text="Відповідь від AI:").grid(row=2, column=0, sticky="w", padx=10)
    
    response_frame = tk.Frame(window)
    response_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
    response_frame.grid_rowconfigure(0, weight=1)
    response_frame.grid_columnconfigure(0, weight=1)

    response_box = tk.Text(response_frame, wrap="word")
    response_box.grid(row=0, column=0, sticky="nsew")

    y_scroll = tk.Scrollbar(response_frame, command=response_box.yview)
    y_scroll.grid(row=0, column=1, sticky="ns")
    response_box.config(yscrollcommand=y_scroll.set)

    # Меню вибору таблиці
    table_var = tk.StringVar(window)
    table_var.set("first_dishes")

    tk.Label(window, text="Зберегти у таблицю:").grid(row=4, column=0, sticky="w", padx=10)
    tk.OptionMenu(window, table_var, "first_dishes", "second_dishes", "sweets", "drinks").grid(row=5, column=0, sticky="w", padx=10)

    def on_ask():
        prompt = prompt_entry.get("1.0", "end").strip()
        if not prompt:
            messagebox.showwarning("Увага", "Поле запиту порожнє!")
            return
        try:
            response = ask_ai(prompt)
            response_box.delete("1.0", "end")
            response_box.insert("1.0", response)
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def on_save():
        text = response_box.get("1.0", "end-1c")  # Повний текст без \n в кінці
        if not text.strip():
            messagebox.showwarning("Увага", "Немає результату для збереження!")
            return

        try:
            print("Збереження повного тексту рецепта:\n", text)
            lines = [l.strip() for l in text.split("\n") if l.strip()]

            # Назва: перший осмислений рядок
            name = next((l for l in lines if l.lower().startswith("назва:")), "")
            if name:
                name = name.replace("Назва:", "").strip()
            else:
                name = lines[0] if lines else "AI Recipe"

            # Інгредієнти: до першої інструкції
            ingredients_lines = []
            start_collecting = False
            for line in lines:
                if any(kw in line.lower() for kw in ["інгредієнт", "склад"]):
                    start_collecting = True
                    continue
                if "пригот" in line.lower() or "зміш" in line.lower() or "подавай" in line.lower():
                    break
                if start_collecting:
                    ingredients_lines.append(line)

            if not ingredients_lines:
                # fallback: беремо всі рядки, де є буліт
                ingredients_lines = [l for l in lines if "-" in l or "•" in l]

            ingredients = "\n".join(ingredients_lines) if ingredients_lines else "Невідомо"

            # Час приготування
            import re
            time_pattern = re.compile(r"\b\d{1,3}\s*(?:хв|хвилин|хвилини|хвилина)\b", re.IGNORECASE)
            time = next((time_pattern.search(l).group(0) for l in lines if time_pattern.search(l)), "Невідомо")

            # Кількість інгредієнтів
            quantity = str(ingredients.count("\n") + 1 if ingredients != "Невідомо" else 0)

            conn = connect_to_db()
            insert_dish(conn, table_var.get(), name, time, ingredients, quantity)

            messagebox.showinfo("Успіх", "Рецепт збережено у базу!")
        except Exception as e:
            messagebox.showerror("Помилка при збереженні", str(e))

    # Кнопки
    button_frame = tk.Frame(window)
    button_frame.grid(row=6, column=0, pady=10)

    tk.Button(button_frame, text="Отримати рецепт", command=on_ask).pack(side="left", padx=5)
    tk.Button(button_frame, text="Зберегти рецепт у БД", command=on_save).pack(side="left", padx=5)

    window.mainloop()
