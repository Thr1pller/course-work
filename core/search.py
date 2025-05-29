def search_dishes(conn, dish_type, keyword, column):
    """Пошук у вказаному dish_type (таблиця) за keyword в колонці name або ingredients."""
    cursor = conn.cursor()
    query = f"SELECT * FROM {dish_type} WHERE {column} LIKE %s"
    cursor.execute(query, (f"%{keyword}%",))
    results = cursor.fetchall()
    cursor.close()
    return results
