def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id};"
    cursor.execute(query)
    return cursor.fetchall()

get_user_data("lil bobby tables")
