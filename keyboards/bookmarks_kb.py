from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from lexicon.lexicon import LEXICON


def create_bookmarks_keyboard(list_bookmarks: list) -> InlineKeyboardBuilder:
    bookmarks_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons_kb = []
    for button in list_bookmarks:
        buttons_kb.append(InlineKeyboardButton(text=f'{button[1]} - {button[0][:100]}',
                                               callback_data=str(button[1])))
    bookmarks_kb.row(*buttons_kb, width=1)
    bookmarks_kb.row(InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'], callback_data='edit_bookmarks'),
                     InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'), width=2)
    return bookmarks_kb


def create_edit_keyboard(list_bookmarks: list) -> InlineKeyboardBuilder:
    bookmarks_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons_kb = []
    for button in list_bookmarks:
        buttons_kb.append(InlineKeyboardButton(text=f'{LEXICON["del"]} {button[1]} - {button[0][:100]}',
                                               callback_data=f'{button[1]}del'))
    bookmarks_kb.row(*buttons_kb, width=1)
    bookmarks_kb.row(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'), width=1)
    return bookmarks_kb
