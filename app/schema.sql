DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS book_log;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  full_name TEXT NOT NULL,
  contact_number INTEGER
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    category TEXT NOT NULL,
    ean_isbn13 TEXT,
    upc_isbn10 TEXT,
    book_desc TEXT,
    publisher TEXT,
    date_published DATE,
    pages INTEGER
);

CREATE TABLE book_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime_log TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    remarks TEXT,
    book_status TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (book_id) REFERENCES book (id)
);