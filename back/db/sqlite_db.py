import json
import sqlite3

tables = '''CREATE TABLE IF NOT EXISTS continents (
     continent_id INTEGER PRIMARY KEY NOT NULL,
     continent TEXT UNIQUE NOT NULL,
     continent_guid TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS countries(
     country_id INTEGER PRIMARY KEY NOT NULL,
     country TEXT UNIQUE NOT NULL,
     continent_id INTERGER NOT NULL,
     country_guid TEXT UNIQUE NOT NULL,
     UNIQUE (country, continent_id),
     FOREIGN KEY (continent_id) REFERENCES continents (continent_id)
);
CREATE TABLE IF NOT EXISTS genders(
     gender_id INTEGER PRIMARY KEY NOT NULL,
     gender TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS genres(
     genre_id INTEGER PRIMARY KEY NOT NULL,
     genre TEXT UNIQUE NOT NULL,
     genre_guid TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS publishers(
     publisher_id INTEGER PRIMARY KEY NOT NULL,
     publisher TEXT UNIQUE NOT NULL,
     publisher_guid TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS themes(
     theme_id INTEGER PRIMARY KEY NOT NULL,
     theme TEXT UNIQUE NOT NULL,
     theme_guid TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS authors(
     author_id INTEGER PRIMARY KEY NOT NULL,
     full_name TEXT UNIQUE NOT NULL,
     birth_year INTEGER,
     death_year INTEGER,
     gender_id INTEGER,
     country_id INTEGER,
     author_guid TEXT UNIQUE NOT NULL,
     FOREIGN KEY (country_id) REFERENCES countries (country_id),
     FOREIGN KEY (gender_id) REFERENCES genders (gender_id)
);
CREATE TABLE IF NOT EXISTS ebooks(
     ebook_id INTEGER PRIMARY KEY NOT NULL,
     title TEXT NOT NULL,
     year_of_publication INTEGER,
     publisher_id INTEGER,
     ebook_guid TEXT UNIQUE NOT NULL,
     inserted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
     is_deleted INTEGER NOT NULL DEFAULT 0,
     FOREIGN KEY (publisher_id) REFERENCES publishers (publisher_id)
);
CREATE INDEX IF NOT EXISTS ebooks_inserted_at ON ebooks(inserted_at);
CREATE TABLE IF NOT EXISTS ebooks_authors(
     ebook_id INTEGER NOT NULL,
     author_id INTEGER NOT NULL,
     PRIMARY KEY (ebook_id, author_id),
     FOREIGN KEY (ebook_id) REFERENCES ebooks (ebook_id),
     FOREIGN KEY (author_id) REFERENCES authors (author_id)
);
CREATE TABLE IF NOT EXISTS ebooks_genres(
     ebook_id INTEGER NOT NULL,
     genre_id INTEGER NOT NULL,
     PRIMARY KEY (ebook_id, genre_id),
     FOREIGN KEY (ebook_id) REFERENCES ebooks (ebook_id),
     FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
);
CREATE TABLE IF NOT EXISTS ebooks_themes(
     ebook_id INTEGER NOT NULL,
     theme_id INTEGER NOT NULL,
     PRIMARY KEY (ebook_id, theme_id),
     FOREIGN KEY (ebook_id) REFERENCES ebooks (ebook_id),
     FOREIGN KEY (theme_id) REFERENCES themes (theme_id)
);
CREATE TABLE IF NOT EXISTS reading_status (
     reading_status_id INTEGER PRIMARY KEY,
     reading_status TEXT UNIQUE NOT NULL
     );
CREATE TABLE IF NOT EXISTS readings (
     reading_id INTEGER PRIMARY KEY,
     ebook_id INTEGER NOT NULL,
     beginning_date TEXT NOT NULL,
     ending_date TEXT,
     reading_status_id INTEGER NOT NULL,
     reading_guid TEXT UNIQUE NOT NULL,
     FOREIGN KEY (ebook_id) REFERENCES ebooks (ebook_id),
     FOREIGN KEY (reading_status_id) REFERENCES reading_status (reading_status_id)
);
CREATE TABLE IF NOT EXISTS reading_lists(
     reading_list_id INTEGER PRIMARY KEY,
     name  TEXT UNIQUE NOT NULL,
     description TEXT,
     items TEXT NOT NULL,
     reading_list_guid  TEXT UNIQUE NOT NULL
);
'''


def connect(db):
     connexion = sqlite3.connect(db)
     connexion.execute('PRAGMA foreign_keys = on;')
     return connexion


if __name__ == '__main__':
     env = None
     with open('back/env.json', 'r') as fr:
          env = json.loads(fr.read())
     db = sqlite3.connect(env["database_test"])
     db.executescript(tables)
     with open(env["database_feed"], 'r', encoding='utf-8') as fr:
          db.executescript(fr.read())
     db.close()