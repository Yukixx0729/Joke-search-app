from database import sql_write,select_one,select_all,edit_one,delete_one

def joke_review(joke_id):
    return select_all(f"SELECT users.name,posts.id,posts.content,posts.rating,posts.joke_id,posts.id FROM posts JOIN users on posts.user_id=users.id WHERE posts.joke_id = {joke_id} ORDER BY posts.id DESC;")

def joke_rating_good(joke_id):
    return select_all(f"SELECT count(posts.rating),joke_id FROM posts WHERE posts.rating='good' and joke_id ={joke_id} GROUP BY joke_id;")

def joke_rating_bad(joke_id):
    return select_all(f"SELECT count(posts.rating),joke_id FROM posts WHERE posts.rating='bad' and joke_id ={joke_id} GROUP BY joke_id;")

def post_review(content,rating,joke_id,user_id):
    sql_write("INSERT INTO posts(content,rating,joke_id,user_id) VALUES (%s,%s,%s,%s);",[content,rating,joke_id,user_id])

def edit_review(review_id):
    return select_one("SELECT users.name,posts.id,posts.content,posts.rating,posts.joke_id,posts.id FROM posts JOIN users on posts.user_id=users.id WHERE posts.id = %s",[review_id])

def edit_review_act(content,rating,post_id):
    edit_one("UPDATE posts SET content=%s,rating=%s WHERE id=%s;",[content,rating,post_id])

def delete_review_act(review_id):
    delete_one("DELETE FROM posts WHERE id=%s;",[review_id])

def top_joke_rating():
    return select_all("SELECT count(posts.rating),joke_id FROM posts WHERE posts.rating='good' GROUP BY joke_id ORDER BY count(posts.rating) DESC LIMIT 3;")

def my_joke_review(user_id):
    return select_all(f"SELECT users.name,posts.content,posts.rating,posts.joke_id,posts.id FROM posts JOIN users on posts.user_id=users.id WHERE posts.user_id = {user_id} ORDER BY posts.id DESC;")

def saved_jokes(joke_id,user_id):
    sql_write("INSERT INTO myfav(joke_id,user_id) VALUES (%s,%s);",[joke_id,user_id])

def all_saved_jokes(user_id):
    return select_all(f"SELECT myfav.joke_id,users.name,users.id FROM myfav JOIN users on myfav.user_id=users.id WHERE myfav.user_id = {user_id}")

def delete_saved_joke(joke_id,user_id):
    delete_one("DELETE FROM myfav WHERE joke_id=%s AND user_id=%s;",[joke_id,user_id])

def insert_text_joke(joke,user_id):
    sql_write("INSERT INTO blog(joke,user_id) VALUES (%s,%s);",[joke,user_id])

def all_jokes():
    return select_all("SELECT users.name,blog.joke,blog.image_url,blog.id,users.id FROM blog JOIN users on blog.user_id=users.id ORDER BY blog.id DESC;")

def all_jokes_by_id(user_id):
    return select_all(f"SELECT blog.id,blog.joke,blog.image_url FROM blog JOIN users on blog.user_id=users.id WHERE users.id = {user_id} ORDER BY blog.id DESC;")

def insert_image_joke(image_url,user_id):
    sql_write("INSERT INTO blog(image_url,user_id) VALUES (%s,%s);",[image_url,user_id])

def edit_jokes_by_id(joke_id):
    return select_one("SELECT * FROM blog WHERE id = %s;",[joke_id])

def edit_joke_act_text(joke,joke_id):
    edit_one("UPDATE blog SET joke=%s WHERE id=%s;",[joke,joke_id])

def edit_joke_act_image(image_url,joke_id):
    edit_one("UPDATE blog SET image_url=%s WHERE id=%s;",[image_url,joke_id])

def delete_joke_act(joke_id):
    delete_one("DELETE FROM blog WHERE id=%s;",[joke_id])

# def rating_post_joke(joke_id,user_id,rating):
#     sql_write("INSERT INTO rating(joke_id,user_id,rating) VALUES (%s,%s,%s);",[joke_id,user_id,rating])