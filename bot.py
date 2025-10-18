import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message, CallbackQuery
from config import BOT_TOKEN, CHANNEL_ID
from keyboards import telefon_button, tasdiqlash_button
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from states import ArizaState

dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await message.answer(f"Salom, {message.from_user.full_name}! 😊\nArizangizni qoldirishingiz mumkin!")  # type:ignore
    await message.answer("Ismingizni kiriting")
    await state.set_state(ArizaState.ism)

@dp.message(StateFilter(ArizaState.ism))
async def ism_handler(message: Message, state: FSMContext):
    await message.answer("Ismingiz qabul qilindi! Familiyangizni kiriting:")
    await state.update_data(ism=message.text)
    await state.set_state(ArizaState.familiya)
    
@dp.message(StateFilter(ArizaState.familiya))
async def familiya_handler(message: Message, state: FSMContext):
    await message.answer("Familiyagiz qabul qilindi! Telefon raqam jo'nating:", reply_markup=telefon_button)
    await state.update_data(familiya=message.text)
    await state.set_state(ArizaState.telefon_raqam)


@dp.message(StateFilter(ArizaState.telefon_raqam))
async def telefon_raqam_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(telefon_raqam=message.contact.phone_number)
        await message.answer("Telefon raqam qabul qilindi! Arizangizni yozing:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ArizaState.ariza)
    except:
        await message.answer("Telefon raqamni to'g'ri jo'nating:", reply_markup=telefon_button)
        await state.set_state(ArizaState.telefon_raqam)


@dp.message(StateFilter(ArizaState.ariza))
async def ariza_handler(message: Message, state:FSMContext):
    await state.update_data(ariza=message.text)
    data = await state.get_data()
    text = (f"YANGI ARIZA:\n\n"
            f"👤  Ism: {data['ism']}\n"
            f"👥  Familiya: {data['familiya']}\n"
            f"📞  Telefon raqam: {data['telefon_raqam']}\n"
            f"📝  Ariza: {data['ariza']}\n"
              )
    await state.update_data(text=text)
    await message.answer(f"{text}\n\nArizangiz to'g'rimi?", reply_markup=tasdiqlash_button)
    await state.set_state(ArizaState.tasdiqlash)


@dp.callback_query(StateFilter(ArizaState.tasdiqlash))
async def tasdiqlash_handler(call: CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        data = await state.get_data()
        await call.message.answer("✅  Arizangiz qabul qilindi, javobimizni kuting! 🎉", reply_markup=ReplyKeyboardRemove())
        mytext = data.get("text")
        await bot.send_message(chat_id=CHANNEL_ID, text=mytext)  # type: ignore
        await state.clear()
        await call.message.answer("Yangi xabar yuborish uchun /start bosing!")
    else:
        await call.message.answer("❌  Arizangiz bekor qilindi.\n\nYangi xabar yuborish uchun /start bosing!")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
