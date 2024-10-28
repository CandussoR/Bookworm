class EbookRepository():
    def __init__(self, conn):
        self.conn = conn
    

    def get_id_from_guid(self, guid):
        id, = self.conn.execute("SELECT ebook_id FROM ebooks WHERE ebook_guid = ?", [guid]).fetchone()
        if not id:
            ValueError("Identifier doesn't exist in database")
        return id
    

    def get_ebook_row_by(self, key, val) :
        '''Gets a row without join either by ebook_id or ebook_guid.'''
        if key in ["ebook_id", "ebook_guid"]:
            return self.conn.execute(
                'SELECT title, publisher_id, year_of_publication, ebook_guid, is_deleted FROM ebooks WHERE ? = ? ;'
                ).fetchone()
        else:
            raise ValueError("Key must be ebook_id or ebook_guid")


    def get_ebooks(self):
        sb = '''WITH et AS (
                    SELECT et.ebook_id, GROUP_CONCAT(t.theme, ', ') as theme
                    FROM ebooks_themes et
                    JOIN themes t ON t.theme_id = et.theme_id
                    GROUP BY ebook_id
                ),
                ea AS (
                    SELECT ea.ebook_id, GROUP_CONCAT(a.full_name, ', ') as author
                    FROM ebooks_authors ea
                    JOIN authors a ON ea.author_id = a.author_id
                    GROUP BY ebook_id
                ),
                eg AS (
                    SELECT eg.ebook_id, GROUP_CONCAT(g.genre, ', ') as genre
                    FROM ebooks_genres eg
                    JOIN genres g ON g.genre_id = eg.genre_id
                    GROUP BY ebook_id
                )
                SELECT e.title, author, e.year_of_publication, p.publisher, genre, theme, e.ebook_guid, e.inserted_at
                FROM ebooks e
                JOIN ea ON ea.ebook_id = e.ebook_id
                JOIN publishers p ON p.publisher_id = e.publisher_id
                LEFT JOIN et ON ea.ebook_id = et.ebook_id
                LEFT JOIN eg ON ea.ebook_id = eg.ebook_id
                WHERE e.is_deleted = 0;
              '''
        return self.conn.execute(sb).fetchall()


    def get_ebook_for_reading_list(self, ebook_id) -> tuple:
        '''We generally have to retrieve the id before making any change in the database so using the id is quite convenient.
           Returns (title, author, year_of_publication, publisher, genre, theme, ebook_guid).
        '''
        sb = f'''WITH ea AS (
            SELECT ea.ebook_id, GROUP_CONCAT(a.full_name, ',') as author
            FROM ebooks_authors ea
            JOIN authors a ON ea.author_id = a.author_id
            WHERE ebook_id = {ebook_id}
        )
        SELECT e.title, author, e.ebook_guid
        FROM ea
        JOIN ebooks e ON ea.ebook_id = e.ebook_id;
        '''
        return self.conn.execute(sb).fetchone()


    def get_ebook(self, ebook_id) -> tuple:
        '''We generally have to retrieve the id before making any change in the database so using the id is quite convenient.
           Returns (title, author, ebook_guid).
        '''
        sb = f'''WITH et AS (
            FROM ebooks_themes et
            JOIN themes t ON t.theme_id = et.theme_id
            WHERE ebook_id = {ebook_id}
        ),
        ea AS (
            SELECT ea.ebook_id, GROUP_CONCAT(a.full_name, ',') as author
            FROM ebooks_authors ea
            JOIN authors a ON ea.author_id = a.author_id
            WHERE ebook_id = {ebook_id}
        ),
        SELECT e.title, author, e.ebook_guid
        FROM ea
        JOIN ebooks e ON ea.ebook_id = e.ebook_id
        '''
        return self.conn.execute(sb).fetchone()


    def create(self, model):
        id, = self.conn.execute(
            "INSERT INTO ebooks (title, year_of_publication, publisher_id, ebook_guid) VALUES (:title, :year_of_publication, :publisher_id, :ebook_guid) RETURNING ebook_id;",
            model.__dict__,
        ).fetchone()
        return id
    

    def update(self, model):
        self.conn.execute('''UPDATE ebooks
                            SET title = :title,
                                year_of_publication = :year_of_publication,
                                publisher_id = :publisher_id
                            WHERE ebook_guid = :ebook_guid;''',
                            [model.__dict__]
        )


    def delete(self, guid, wipe = False):
        if wipe:
            self.conn.execute("DELETE FROM ebooks WHERE ebook_guid = ?", [guid])
        else:
            self.conn.execute("UPDATE ebooks SET is_deleted = 1 WHERE ebook_guid = ?", [guid])


    def get_ebooks_by(self, key, value):
        match key:
            case "continent":
                return self.get_ebooks_by_continent(value)
            case "country":
                return self.get_ebooks_by_country(value)
            case "author":
                return self.get_ebooks_by_author(value)
            case "genre":
                return self.get_ebooks_by_genre(value)
            case "theme" :
                return self.get_ebooks_by_theme(value)
            case "gender":
                raise NotImplemented("Not yet done")
            case _:
                raise ValueError("Invalid key.")
    

    def get_ebooks_by_continent(self, name) :
        '''To be debugged, probably, when times come.'''
        query = '''WITH ic AS (
                    SELECT DISTINCT e.ebook_id, c2.country
                    FROM continents c1
                    JOIN countries c2 ON c2.continent_id = c1.continent_id
                    JOIN authors a ON a.country_id = c2.country_id
                    JOIN ebooks_authors ea ON a.author_id = ea.author_id
                    JOIN ebooks e ON e.ebook_id = ea.ebook_id
                    WHERE continents.continent = ?
                    ),
                    (
                        SELECT et.ebook_id, GROUP_CONCAT(t.theme, ', ') as theme
                        FROM ic
                        JOIN ebooks_themes et ON ic.ebook_id = et.ebook_id
                        JOIN themes t ON t.theme_id = et.theme_id
                        GROUP BY ebook_id
                    ),
                    ea AS (
                        SELECT ea.ebook_id, GROUP_CONCAT(a.full_name, ', ') as author
                        FROM ic
                        JOIN ebooks_authors ea ON ea.ebook_id = ic.ebook_id
                        JOIN authors a ON ea.author_id = a.author_id
                        GROUP BY ebook_id
                    ),
                    eg AS (
                        SELECT eg.ebook_id, GROUP_CONCAT(g.genre, ', ') as genre
                        FROM ic
                        JOIN ebooks_genres eg ON ic.ebook_id = eg.ebook_id
                        JOIN genres g ON g.genre_id = eg.genre_id
                        GROUP BY ebook_id
                    )
                    SELECT e.title, author, e.year_of_publication, p.publisher, genre, theme, country, e.ebook_guid
                    FROM ic
                    JOIN ea ON ic.ebook_id = ea.ebook_id
                    JOIN ebooks e ON ea.ebook_id = e.ebook_id
                    JOIN publishers p ON p.publisher_id = e.publisher_id
                    JOIN et ON ea.ebook_id = et.ebook_id
                    JOIN eg ON ea.ebook_id = eg.ebook_id;
                '''
        return self.conn.execute(query, [name]).fetchall()
    

    def get_ebooks_by_country(self, name) :
        '''To be debugged, probably, when time comes.'''
        query = '''WITH ic AS (
                    SELECT DISTINCT e.ebook_id, c.country
                    FROM countries c
                    JOIN authors a ON a.country_id = c.country_id
                    JOIN ebooks_authors ea ON a.author_id = ea.author_id
                    JOIN ebooks e ON e.ebook_id = ea.ebook_id
                    WHERE c.country = ?
                    ),
                    (
                        SELECT et.ebook_id, GROUP_CONCAT(t.theme, ',') as theme
                        FROM ic
                        JOIN ebooks_themes et ON ic.ebook_id = et.ebook_id
                        JOIN themes t ON t.theme_id = et.theme_id
                        GROUP BY ebook_id
                    ),
                    ea AS (
                        SELECT ea.ebook_id, GROUP_CONCAT(a.full_name, ',') as author
                        FROM ic
                        JOIN ebooks_authors ea ON ea.ebook_id = ic.ebook_id
                        JOIN authors a ON ea.author_id = a.author_id
                        GROUP BY ebook_id
                    ),
                    eg AS (
                        SELECT eg.ebook_id, GROUP_CONCAT(g.genre, ',') as genre
                        FROM ic
                        JOIN ebooks_genres eg ON ic.ebook_id = eg.ebook_id
                        JOIN genres g ON g.genre_id = eg.genre_id
                        GROUP BY ebook_id
                    )
                    SELECT e.title, author, e.year_of_publication, p.publisher, genre, theme, country, e.ebook_guid
                    FROM ic
                    JOIN ea ON ic.ebook_id = ea.ebook_id
                    JOIN ebooks e ON ea.ebook_id = e.ebook_id
                    JOIN publishers p ON p.publisher_id = e.publisher_id
                    JOIN et ON ea.ebook_id = et.ebook_id
                    JOIN eg ON ea.ebook_id = eg.ebook_id;
                '''
        return self.conn.execute(query, [name]).fetchall()
    

    def get_ebooks_by_author(self, name):
        '''Correct one'''
        query = '''WITH id AS (
                        SELECT author_id
                        FROM authors
                        WHERE full_name = ?
                    ),
                    ebook_ids AS (
                        SELECT ea.ebook_id
                        FROM id
                            JOIN ebooks_authors ea ON ea.author_id = id.author_id
                    ),
                    ebooks_with_authors AS (
                        SELECT ei.ebook_id,
                            GROUP_CONCAT(a.full_name, ',') as author
                        FROM ebook_ids ei
                            JOIN ebooks_authors ea ON ei.ebook_id = ea.ebook_id
                            JOIN authors a ON ea.author_id = a.author_id
                        GROUP BY ei.ebook_id
                    ),
                    ebooks_with_themes AS (
                        SELECT ei.ebook_id,
                            GROUP_CONCAT(t.theme, ',') as theme
                        FROM ebook_ids ei
                            JOIN ebooks_themes et ON ei.ebook_id = et.ebook_id
                            JOIN themes t ON t.theme_id = et.theme_id
                        GROUP BY ei.ebook_id
                    ),
                    ebooks_with_genres AS (
                        SELECT ei.ebook_id,
                            GROUP_CONCAT(g.genre, ',') as genre
                        FROM ebook_ids ei
                            JOIN ebooks_genres eg ON ei.ebook_id = eg.ebook_id
                            JOIN genres g ON g.genre_id = eg.genre_id
                        GROUP BY ei.ebook_id
                    )
                    SELECT e.title,
                        ea.author,
                        e.year_of_publication,
                        p.publisher,
                        eg.genre,
                        et.theme,
                        e.ebook_guid
                    FROM ebook_ids ei
                        JOIN ebooks e ON ei.ebook_id = e.ebook_id
                        JOIN publishers p ON p.publisher_id = e.publisher_id
                        JOIN ebooks_with_authors ea ON ei.ebook_id = ea.ebook_id
                        JOIN ebooks_with_genres eg ON ei.ebook_id = eg.ebook_id
                        JOIN ebooks_with_themes et ON ei.ebook_id = et.ebook_id;
                '''
        return self.conn.execute(query, [name])
    

    def get_ebooks_by_genre(self, name):
        '''Correct one.'''
        query = '''WITH id AS (
                        SELECT genre_id
                        FROM genres
                        WHERE genre = ?
                    ),
                    ebook_ids AS (
                        SELECT ebook_id
                        FROM id
                            JOIN ebooks_genres eg ON id.genre_id = eg.genre_id
                    ),
                    ebooks_with_genres AS (
                        SELECT ei.ebook_id,
                            GROUP_CONCAT(g.genre, ',') as genre
                        FROM ebook_ids ei
                            JOIN ebooks_genres eg ON ei.ebook_id = eg.ebook_id
                            JOIN genres g ON g.genre_id = eg.genre_id
                        GROUP BY ei.ebook_id
                    ),
                    ebooks_with_authors AS (
                        SELECT ei.ebook_id,
                            GROUP_CONCAT(a.full_name, ',') as author
                        FROM ebook_ids ei
                            JOIN ebooks_authors ea ON ei.ebook_id = ea.ebook_id
                            JOIN authors a ON ea.author_id = a.author_id
                        GROUP BY ei.ebook_id
                    ),
                    ebooks_with_themes AS (
                        SELECT ei.ebook_id,
                            GROUP_CONCAT(t.theme, ',') as theme
                        FROM ebook_ids ei
                            JOIN ebooks_themes et ON ei.ebook_id = et.ebook_id
                            JOIN themes t ON t.theme_id = et.theme_id
                        GROUP BY ei.ebook_id
                    )
                    SELECT e.title,
                        author,
                        e.year_of_publication,
                        p.publisher,
                        genre,
                        theme,
                        e.ebook_guid
                    FROM ebook_ids ei
                        JOIN ebooks e ON ei.ebook_id = e.ebook_id
                        JOIN publishers p ON p.publisher_id = e.publisher_id
                        JOIN ebooks_with_authors ea ON ei.ebook_id = ea.ebook_id
                        JOIN ebooks_with_genres eg ON ei.ebook_id = eg.ebook_id
                        JOIN ebooks_with_themes et ON ei.ebook_id = et.ebook_id;'''
        return self.conn.execute(query, [name]) 


    def get_ebooks_by_theme(self, name):
        '''Correct one, tested'''
        query = '''WITH id AS (
                        SELECT theme_id
                        FROM themes
                        WHERE theme = ?
                    ),
                    ebooks_id AS (
                        SELECT et.ebook_id
                        FROM ebooks_themes et
                            JOIN id ON id.theme_id = et.theme_id
                    ),
                    ebooks_with_themes AS (
                        SELECT ei.ebook_id,
                            GROUP_CONCAT(t.theme, ',') as theme
                        FROM ebooks_id ei
                            JOIN ebooks_themes et ON et.ebook_id = ei.ebook_id
                            JOIN themes t ON et.theme_id = t.theme_id
                    ),
                    ebooks_with_genres AS (
                        SELECT ei.ebook_id,
                            GROUP_CONCAT(g.genre, ',') as genre
                        FROM ebooks_id ei
                            JOIN ebooks_genres eg ON eg.ebook_id = ei.ebook_id
                            JOIN genres g ON g.genre_id = eg.genre_id
                        GROUP BY ei.ebook_id
                    ),
                    ebooks_with_authors AS (
                        SELECT ei.ebook_id,
                            GROUP_CONCAT(a.full_name, ',') as author
                        FROM ebooks_id ei
                        JOIN ebooks_authors ea ON ei.ebook_id = ea.ebook_id
                        JOIN authors a ON ea.author_id = a.author_id
                        GROUP BY ei.ebook_id
                    )
                    SELECT e.title, ea.author, e.year_of_publication, p.publisher, eg.genre, et.theme, e.ebook_guid
                    FROM ebooks_id ei
                    JOIN ebooks e ON e.ebook_id = ei.ebook_id
                    JOIN publishers p ON p.publisher_id = e.publisher_id
                    JOIN ebooks_with_authors ea ON ei.ebook_id = ea.ebook_id
                    JOIN ebooks_with_genres eg ON ei.ebook_id = eg.ebook_id
                    JOIN ebooks_with_themes et ON ei.ebook_id = et.ebook_id;'''
        return self.conn.execute(query, [name])
    

    def search(self, query):
        param = f'%{query}%'
        data = self.conn.execute(f'''
                          WITH matches as (
                            SELECT ebook_id, title, ebook_guid
                            FROM ebooks
                            WHERE title LIKE \'{param}\'
                          )
                          SELECT m.title, GROUP_CONCAT(a.full_name, ',') as author, m.ebook_guid
                          FROM matches m
                          JOIN ebooks_authors ea ON ea.ebook_id = m.ebook_id
                          JOIN authors a ON a.author_id = ea.author_id;''').fetchall()
        print(data, type(data), data == [(None, None, None)])
        return data if data != [(None, None, None)] else None