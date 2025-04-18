import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

TOKEN = '6451666422:AAGmAt_MdaQAtvIwWuC2Pg1_58ZcnZgJHZg'

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    waiting_for_input = State()

# Старт
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎎 Згенерувати ляльку", callback_data="generate_doll")]
    ])
    await message.answer("Привіт! Я допоможу згенерувати унікальну ляльку 😊", reply_markup=keyboard)

# Кнопка "Згенерувати ляльку"
@dp.callback_query(F.data == "generate_doll")
async def ask_subscription(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Підписатись на @channel1", url="https://t.me/channel1")],
        [InlineKeyboardButton(text="🔗 Підписатись на @channel2", url="https://t.me/channel2")],
        [InlineKeyboardButton(text="✅ Я підписався", callback_data="check_subscription")]
    ])
    await callback.message.answer("Щоб продовжити, підпишись на всі канали:", reply_markup=keyboard)

# "Я підписався"
@dp.callback_query(F.data == "check_subscription")
async def fake_check(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("❌ Ви ще не підписалися на всі канали!")
    await asyncio.sleep(15 * 60)
    await callback.message.answer("✅ Добре, очікуй 15 хвилин, поки генерується лялька ⏳")
    await asyncio.sleep(15 * 60)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔹 Ввести дані для ляльки", callback_data="input_data")]
    ])
    await callback.message.answer("Готово! Натисни кнопку нижче, щоб ввести дані.", reply_markup=keyboard)

# Натискання на "Ввести дані"
@dp.callback_query(F.data == "input_data")
async def ask_input(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи ім’я та бажані аксесуари для ляльки:")
    await state.set_state(Form.waiting_for_input)

# Отримуємо дані → видаємо фейкову помилку
@dp.message(Form.waiting_for_input)
async def fake_generation(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("😓 Упс! Сервер перевантажений. Спробуй пізніше.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
