import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp

# API Tokenlarni joylashtiring
BOT_TOKEN = "BU_YERGA_BOTFATHER_BERGAN_TOKENNI_YASHLANG"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Web App tugmasi orqali siz yaratgan saytni to'g'ridan-to'g'ri Telegram ichida ochish
    kb = [
        [types.InlineKeyboardButton(text="AI Chatni ochish", web_app=types.WebAppInfo(url="https://haxi-ai-uzb.netlify.app/"))]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Sizga qanday yordam bera olaman? Quyidagi tugma orqali to'liq interfeysdan foydalanishingiz mumkin:", reply_markup=keyboard)

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    
    # "O'ylamoqda..." statusini ko'rsatish
    waiting_msg = await message.answer("✏️...")
    
    # Bepul AI API-siga so'rov yuborish
    async with aiohttp.ClientSession() as session:
        payload = {
            "model": "meta-llama/llama-3-8b-instruct:free",
            "messages": [{"role": "user", "content": user_text}]
        }
        headers = {"Content-Type": "application/json"}
        
        try:
            async with session.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers) as resp:
                data = await resp.json()
                ai_answer = data['choices'][0]['message']['content']
                await waiting_msg.edit_text(ai_answer)
        except Exception:
            await waiting_msg.edit_text("Hozircha javob berishda xatolik yuz berdi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
