DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email TEXT NOT NULL,
    city VARCHAR(20)NOT NULL,
    admin boolean NOT NULL,
    password_hash TEXT NOT NULL
);

DROP TABLE IF EXISTS posts CASCADE;

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    rating TEXT ,
    joke_id INT NOT NULL,
    user_id INT,
    CONSTRAINT fk_user_posts
        FOREIGN KEY (user_id)
        REFERENCES users(id)
);

DROP TABLE IF EXISTS myfav CASCADE;
CREATE TABLE myfav (
    id SERIAL PRIMARY KEY,
    joke_id INT NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT fk_user_myfav
        FOREIGN KEY (user_id)
        REFERENCES users(id)
);

DROP TABLE IF EXISTS blog CASCADE;
CREATE TABLE blog (
    id SERIAL PRIMARY KEY,
    image_url TEXT ,
    joke TEXT ,
    user_id INT NOT NULL,
    CONSTRAINT fk_user_blog
        FOREIGN KEY (user_id)
        REFERENCES users(id)
);

-- DROP TABLE IF EXISTS likes CASCADE;
-- CREATE TABLE likes (
--     id SERIAL PRIMARY KEY,
--     joke_id INT NOT NULL,
--     user_id INT NOT NULL,
--     rating boolean NOT NULL,
--     CONSTRAINT fk_blog_likes
--         FOREIGN KEY (joke_id)
--         REFERENCES blog(id),
--     CONSTRAINT fk_user_likes
--         FOREIGN KEY (user_id)
--         REFERENCES users(id)
-- );