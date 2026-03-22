import asyncio
import ssl
import certifi
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.client.session.aiohttp import AiohttpSession
from database import init_db, give_starter_duck

TOKEN = "8725402813:AAHc2Z3h7gigI9hwoEr-8iemB9M5579ruTM" # 

async def main():
    # Настройка сессии для обхода ошибки SSL
    session = AiohttpSession()
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()
    db_conn = init_db()

    @dp.message(CommandStart())
    async def start(message: types.Message):
        user_id = message.from_user.id
        cursor = db_conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (user_id, food) VALUES (?, ?)", (user_id, 1000))
            give_starter_duck(user_id)
            db_conn.commit()
            await message.answer("🕶 Добро пожаловать в банду! Лови 1000 корма.")
        
        # Кнопка для игры
        kb = [[types.InlineKeyboardButton(text="🕶 ИГРАТЬ", web_app=types.WebAppInfo(url="https://opupenchikklass-lab.github.io/duck-game/"))]]
        markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer("Твои утки ждут тебя:", reply_markup=markup)

    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())