from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message

from database.db import (conn, cursor, db_table_val, dp_bookmarks,
                         dp_id_bookmark, dp_number_page_check)
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    cursor.execute('SELECT user_id FROM book_bot_db WHERE user_id = ?', (message.from_user.id,))
    if cursor.fetchone() is None:
        db_table_val(user_id=message.from_user.id)


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON[message.text])


@router.message(Command(commands=['beginning']))
async def process_beginning_command(message: Message):
    cursor.execute('UPDATE book_bot_db SET page = 1 WHERE user_id = ?', (message.from_user.id,))
    conn.commit()
    text = book[1]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard('backward', f'{1}/{len(book)}', 'forward').as_markup())


@router.message(Command(commands=['continue']))
async def process_continue_command(message: Message):
    cursor.execute('SELECT page FROM book_bot_db WHERE user_id = ?', (message.from_user.id,))
    number = cursor.fetchone()[0]
    text = book[number]
    await message.answer(text=text,
                         reply_markup=create_pagination_keyboard('backward', f'{number}/{len(book)}',
                                                                 'forward').as_markup())


@router.message(Command(commands=['bookmarks']))
async def process_bookmarks_command(message: Message):
    list_bookmarks = dp_bookmarks(message.from_user.id)
    if list_bookmarks:
        await message.answer(text=LEXICON[message.text],
                             reply_markup=create_bookmarks_keyboard(list_bookmarks).as_markup())
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery):
    cursor.execute('SELECT page FROM book_bot_db WHERE user_id = ?', (callback.from_user.id,))
    number = cursor.fetchone()[0]
    if number < len(book):
        cursor.execute('UPDATE book_bot_db SET page = page + 1 WHERE user_id = ?', (callback.from_user.id,))
        conn.commit()
        text = book[number + 1]
        await callback.message.edit_text(text=text, reply_markup=create_pagination_keyboard(
            'backward', f'{number + 1}/{len(book)}', 'forward').as_markup())
        await callback.answer()


@router.callback_query(Text(text='backward'))
async def process_backward_press(callback: CallbackQuery):
    cursor.execute('SELECT page FROM book_bot_db WHERE user_id = ?', (callback.from_user.id,))
    number = cursor.fetchone()[0]
    if number > 1:
        cursor.execute('UPDATE book_bot_db SET page = page - 1 WHERE user_id = ?', (callback.from_user.id,))
        conn.commit()
        text = book[number - 1]
        await callback.message.edit_text(text=text, reply_markup=create_pagination_keyboard(
            'backward', f'{number - 1}/{len(book)}', 'forward').as_markup())
        await callback.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    number = int(callback.data.split('/')[0])
    cursor.execute('SELECT id FROM book_bot_db WHERE user_id = ?', (callback.from_user.id,))
    id = cursor.fetchone()[0]
    pages = (number_page[0] for number_page in dp_number_page_check(callback.from_user.id))
    if number not in pages:
        cursor.execute('INSERT INTO bookmarks (bookmark, number_page) VALUES (?, ?)', (book[number], number))
        conn.commit()
        cursor.execute('SELECT id FROM bookmarks WHERE bookmark = ?', (book[number],))
        id_bookmark = cursor.fetchone()[0]
        cursor.execute('INSERT INTO book_bot_db_bookmarks (book_id, bookmark_id) VALUES (?, ?)', (id, id_bookmark))
        conn.commit()
        await callback.answer('Страница добавлена в закладки!')
    else:
        await callback.answer('Эта страница уже добавлена в закладки!')


@router.callback_query(lambda x: x.data.isdigit())
async def process_bookmark_press(callback: CallbackQuery):
    number = int(callback.data)
    text = book[number]
    cursor.execute('UPDATE book_bot_db SET page = ? WHERE user_id = ?', (number, callback.from_user.id))
    conn.commit()
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_keyboard(
                                         'backward', f'{number}/{len(book)}', 'forward').as_markup())
    await callback.answer()


@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON[callback.data],
                                     reply_markup=create_edit_keyboard(dp_bookmarks(callback.from_user.id)).as_markup())
    await callback.answer()


@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


@router.callback_query(lambda x: 'del' in x.data and x.data[:-3].isdigit())
async def process_del_bookmark_press(callback: CallbackQuery):
    list_bookmarks = dp_bookmarks(callback.from_user.id)
    if list_bookmarks:
        id = dp_id_bookmark(callback.from_user.id, int(callback.data[:-3]))
        cursor.execute('DELETE FROM bookmarks '
                       'WHERE id = ?', (id,))
        conn.commit()
        await callback.message.edit_text(text=LEXICON['/bookmarks'],
                                         reply_markup=create_edit_keyboard(dp_bookmarks(callback.from_user.id)).as_markup())
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()
