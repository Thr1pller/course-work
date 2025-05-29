ALLOWED_TABLES = {"first_dishes", "second_dishes", "sweets", "drinks"}

def insert_dish(conn, dish_type, name, time_cooking, ingredients, quantity):
    """Додає нову страву до відповідної таблиці."""
    if dish_type not in ALLOWED_TABLES:
        raise ValueError("Недопустима таблиця!")

    with conn.cursor() as cursor:
        query = f"""
            INSERT INTO {dish_type} (name, time_cooking, ingredients, quantity)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, time_cooking, ingredients, quantity))
        conn.commit()

def delete_dish(conn, dish_type, name):
    """Видаляє страву з таблиці за назвою."""
    if dish_type not in ALLOWED_TABLES:
        raise ValueError("Недопустима таблиця!")

    with conn.cursor() as cursor:
        query = f"DELETE FROM {dish_type} WHERE name = %s"
        cursor.execute(query, (name,))
        conn.commit()

def fetch_dishes(conn, dish_type):
    """Повертає всі страви з конкретної таблиці."""
    if dish_type not in ALLOWED_TABLES:
        raise ValueError("Недопустима таблиця!")

    with conn.cursor() as cursor:
        query = f"SELECT * FROM {dish_type}"
        cursor.execute(query)
        return cursor.fetchall()
