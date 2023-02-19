<h1>books_reads_bot</h1>

<ul>
  <li>Создать файл .env, добавить туда токен бота(пример в файле .env_example)</li>
  <li>Создать таблицы в SQlite3</li>
  <br>
  <p>Первая таблица: book_bot_db<p>
  <p>Стоблцы: id(Первичный ключ), user_id(INT), page(INT)<p>
  <p>Вторая таблица: bookmarks<p>
  <p>Стоблцы: id(Первичный ключ), bookmark(TEXT), number_page(INT)<p>
  <p>Третия таблица: book_bot_db_bookmarks<p>
  <p>Стоблцы: id(Первичный ключ), book_id(Foreign key связан с таблицей book_bot_db, столбец id), bookmark_id(Foreign key связан с таблицей bookmarks, столбец id)<p></ul>
