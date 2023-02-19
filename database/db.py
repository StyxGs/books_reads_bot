import sqlite3

conn = sqlite3.connect(r'database\database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int) -> None:
    cursor.execute('INSERT INTO book_bot_db (user_id, page) VALUES (?, ?)', (user_id, None))
    conn.commit()
    return


def dp_bookmarks(user_id: int) -> list[int]:
    cursor.execute('SELECT bookmark, number_page FROM bookmarks INNER JOIN book_bot_db_bookmarks '
                   'ON bookmarks.id = book_bot_db_bookmarks.bookmark_id '
                   'INNER JOIN book_bot_db '
                   'ON book_bot_db.id = book_bot_db_bookmarks.book_id '
                   'WHERE book_bot_db.user_id = ?', (user_id,))
    return cursor.fetchall()


def dp_id_bookmark(user_id: int, number_page: int) -> tuple[int]:
    cursor.execute('SELECT bookmarks.id FROM bookmarks INNER JOIN book_bot_db_bookmarks '
                   'ON bookmarks.id = book_bot_db_bookmarks.bookmark_id '
                   'INNER JOIN book_bot_db '
                   'ON book_bot_db.id = book_bot_db_bookmarks.book_id '
                   'WHERE book_bot_db.user_id = ? and bookmarks.number_page = ?', (user_id, number_page,))
    return cursor.fetchone()


def dp_number_page_check(user_id: int) -> list[int]:
    cursor.execute('SELECT number_page FROM bookmarks INNER JOIN book_bot_db_bookmarks '
                   'ON bookmarks.id = book_bot_db_bookmarks.bookmark_id '
                   'INNER JOIN book_bot_db '
                   'ON book_bot_db.id = book_bot_db_bookmarks.book_id '
                   'WHERE book_bot_db.user_id = ?', (user_id,))
    return cursor.fetchall()
