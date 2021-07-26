DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  category TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  product_name TEXT NOT NULL,
  description TEXT NOT NULL,
  pic_name0 STRING NOT NULL,
  pic_name1 STRING NOT NULL,
  pic_name2 STRING NOT NULL,
  recommend STRING NOT NULL,
  accessories STRING NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (category) REFERENCES category (cat_name)
);

CREATE TABLE category (
  cat_name TEXT PRIMARY KEY UNIQUE NOT NULL
);