import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os

API_TOKEN = os.getenv("BOT_TOKEN", "7216222305:AAFGz_GZFhZtlgZMpkO69Unv-zrktXLd4u0")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_states = {}

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton("Да"))

oracle_answers = [
    "✅ *Да, это случится!*",
    "❌ *Нет, этому не бывать!*",
    "🌫️ *Туман окутал Иерусалим... Свет сердца твоего покажет верный путь! Ступай!*"
]

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("🔮 *Оракул из Иерусалима пробудился...*", parse_mode="Markdown")
    await asyncio.sleep(1.5)
    await message.answer("🕯️ Я вижу будущее сквозь пески времени...", parse_mode="Markdown")
    await asyncio.sleep(1.5)
    await message.answer("📜 И предскажу тебе его... *если осмелишься спросить.*\n\nНачнем?", parse_mode="Markdown", reply_markup=start_keyboard)
    user_states[message.from_user.id] = {"step": "awaiting_start"}

@dp.message_handler(lambda msg: user_states.get(msg.from_user.id, {}).get("step") == "awaiting_start" and msg.text == "Да")
async def ask_name(message: types.Message):
    await message.answer("📛 Назови себя, странник.\n*Как имя твоё, что вписано в Книгу Времен?*", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    user_states[message.from_user.id]["step"] = "awaiting_name"

@dp.message_handler(lambda msg: user_states.get(msg.from_user.id, {}).get("step") == "awaiting_name")
async def ask_event(message: types.Message):
    user_states[message.from_user.id]["name"] = message.text
    await message.answer(f"🖋️ *{message.text}...* Да, помню это имя, оно звучало в веках.", parse_mode="Markdown")
    await asyncio.sleep(1.5)
    await message.answer("✉️ Введи теперь событие, что тревожит твоё сердце.", parse_mode="Markdown")
    user_states[message.from_user.id]["step"] = "awaiting_event"

@dp.message_handler(lambda msg: user_states.get(msg.from_user.id, {}).get("step") == "awaiting_event")
async def reveal_prophecy(message: types.Message):
    await message.answer("🌀 *Я взываю к звёздам... Проникаю в завесу судеб...*", parse_mode="Markdown")
    await asyncio.sleep(2)
    prophecy = random.choice(oracle_answers)
    await message.answer(f"🔔 *Оракул вещает:*\n\n{prophecy}", parse_mode="Markdown")
    user_states.pop(message.from_user.id, None)

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())


