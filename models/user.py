from database import sql_write,select_one,select_all,edit_one,delete_one

def insert_user(name, email,city,admin,password_hash):
    sql_write("INSERT INTO users (name, email,city,admin,password_hash) VALUES (%s, %s, %s, %s,%s)",
    [name, email,city,admin,password_hash])


def login(email):
    return select_one("SELECT * FROM users WHERE email=%s;",[email])

def admin_page():
    return select_all("SELECT * FROM users ORDER BY id ASC;")

def edit_user(user_id):
    return select_one("SELECT * FROM users WHERE id=%s;",[user_id])

def edit_act(name,email,city,admin,id):
    edit_one("UPDATE users SET name=%s,email=%s,city=%s,admin=%s WHERE id=%s;",[name,email,city,admin,id])

def delete_user(user_id):
    return select_one("SELECT id,name,email,city,admin FROM users WHERE id=%s;",[user_id])

def delete_act(id):
    delete_one("DELETE FROM users WHERE id=%s;",[id])

def user_edit_act(name,city,id):
    edit_one("UPDATE users SET name=%s,city=%s WHERE id=%s;",[name,city,id])

def change_password(password_hash,user_id):
    edit_one('UPDATE users SET password_hash=%s WHERE id=%s;',[password_hash,user_id])