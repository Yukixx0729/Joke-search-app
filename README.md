# Jokes Search app(Python full stack app)

## Description

Joke search app is a full stack app that allow users to search the jokes by keywords and type, which is connected with two APIs (the weather API and the jokes' API). Also, users are able to sign up to have more features,such as posting comments and their own jokes, manage their personal information, post contents via the setting section.

## Structure

This app is mainly based on Python Flask ,HTML ,SQL database and Cloudinary. The joke_app database contains 4 tables and uses Cloudinary to store and generate the image urls.

- users table : to storage the users' information
- posts table : to storage the comments users posted
- myfav table : to storage the jokes that users saved
- blog table : to storage the jokes(text or image/gif) the users posted

Beside the users table, all other three tables contain the foreign key which is connected to the users table.

## Standout features

- Users are able to change their personal details including password(except email address);
- Users are able to edit or delete all the comments and jokes they posted;
- Users are able to pick the type of joke(text/image) they want to post;
- Top 3 jokes page is able to count the 3 jokes gainning the most thumb ups;
- Admin account is able to edit/delte all the users,comments and posts;
- If the user doesn't log in, he will still be able to do the joke search and check on the comments or posts;
