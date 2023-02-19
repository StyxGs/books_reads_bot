from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from lexicon.lexicon import LEXICON


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardBuilder:
    pagination_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    pagination_kb.row(
        *[InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button, callback_data=button)
          for button in buttons]
    )
    return pagination_kb
