from aiogram import Router
from aiogram.types import Message

router: Router = Router()


@router.message()
async def send_message_other(message: Message):
    await message.answer('Я создан только для чтения книги(')
