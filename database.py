import psycopg2

def sql_write(query,params):
    conn = psycopg2.connect("dbname=joke_app")
    cursor = conn.cursor()
    cursor.execute(query,params)
    conn.commit()
    cursor.close()
    conn.close()


def select_one(query,params):
    conn = psycopg2.connect("dbname=joke_app")
    cursor = conn.cursor()
    cursor.execute(query,params)
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def select_all(query):
    conn = psycopg2.connect("dbname=joke_app")
    cursor = conn.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def edit_one(query,params):
    conn = psycopg2.connect("dbname=joke_app")
    cursor = conn.cursor()
    cursor.execute(query,params)
    conn.commit()
    cursor.close()
    conn.close()

def delete_one(query,params):
    conn = psycopg2.connect("dbname=joke_app")
    cursor = conn.cursor()
    cursor.execute(query,params)
    conn.commit()
    cursor.close()
    conn.close()