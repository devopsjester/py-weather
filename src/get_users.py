def get_user_data(user_id):
    query = "SELECT * FROM users WHERE id = %s;"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

get_user_data("lil bobby tables")
