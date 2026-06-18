import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp

BOT_TOKEN = "8710679355:AAEVKcdbbaZ79XLDDM2xmGgqTLWIrugIfOQ"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [[types.InlineKeyboardButton(text="AI Chatni ochish", web_app=types.WebAppInfo(url="https://haxi-ai-uzb.netlify.app/"))]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    
    text = (
        "🤖 **Bepul AI Tizimiga xush kelibsiz!**\n\n"
        "✍️ **Matnli chat:** Shunchaki savolingizni yozing.\n"
        "🖼 **AI Rasm:** `/img mushuk kosmosda` deb yozing.\n"
        "🎥 **AI Video:** `/video uchyotgan mashina` deb yozing."
    )
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

# 1. AI RASM GENERATSIYASI
@dp.message(Command("img"))
async def make_image(message: types.Message):
    prompt = message.text.replace("/img", "").strip()
    if not prompt:
        return await message.answer("Rasm uchun biror nima yozing. Misol: `/img kelajak shahri`")
    
    waiting = await message.answer("🎨 Rasm chizilyapti, kuting...")
    
    # Pollinations AI - toza, tekin va nomsiz rasm API
    image_url = f"https://image.pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
    
    try:
        await message.answer_photo(photo=image_url, caption=f"✨ So'rov: {prompt}")
        await waiting.delete()
    except Exception:
        await waiting.edit_text("❌ Rasmni yuklashda xatolik bo'ldi.")

# 2. AI VIDEO GENERATSIYASI
@dp.message(Command("video"))
async def make_video(message: types.Message):
    prompt = message.text.replace("/video", "").strip()
    if not prompt:
        return await message.answer("Video uchun biror nima yozing. Misol: `/video kosmik kema`")
    
    waiting = await message.answer("🎥 Video tayyorlanyapti (10-15 soniya vaqt olishi mumkin)...")
    
    # Pollinations AI Video (Harakatlanuvchi tasvirlar) API
    video_url = f"https://image.pollinations.ai/p/{prompt.replace(' ', '%20')}?width=512&height=512&nologo=true&feed=true"
    
    try:
        await message.answer_video(video=video_url, caption=f"🎬 Video: {prompt}")
        await waiting.delete()
    except Exception:
        await waiting.edit_text("❌ Videoni tayyorlashda xatolik bo'ldi.")

# 3. ODDIY CHAT
@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    waiting_msg = await message.answer("✏️...")
    async with aiohttp.ClientSession() as session:
        payload = {"model": "meta-llama/llama-3-8b-instruct:free", "messages": [{"role": "user", "content": user_text}]}
        headers = {"Content-Type": "application/json"}
        try:
            async with session.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers) as resp:
                data = await resp.json()
                await waiting_msg.edit_text(data['choices'][0]['message']['content'])
        except Exception:
            await waiting_msg.edit_text("Xatolik yuz berdi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
