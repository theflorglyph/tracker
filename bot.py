import asyncio
import logging
import os
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEB_APP_URL = os.environ["WEB_APP_URL"]
PORT = int(os.environ.get("PORT", 8080))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

BTN_TRACKER = "📱 Трекер брендов"
BTN_KEYWORDS = "🇨🇳 Слова для поиска"
BTN_TEMPLATES = "📦 Фразы продавцу"

def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_TRACKER, web_app=WebAppInfo(url=WEB_APP_URL))],
            [KeyboardButton(text=BTN_KEYWORDS), KeyboardButton(text=BTN_TEMPLATES)],
        ],
        resize_keyboard=True,
    )

@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Это твой трекер для закупок Goofish → Авито.\n\n"
        "Открой трекер кнопкой ниже: там бренды по категориям, поиск, "
        "запросы на китайском и заметки по ликвидности.",
        reply_markup=main_keyboard(),
    )

@dp.message(F.text == BTN_KEYWORDS)
async def show_keywords(message: Message) -> None:
    await message.answer(
        "*Слова для поиска на Goofish* (ставь в начало запроса):\n\n"
        "• `中古` — винтаж и архив\n"
        "• `复古` — ретро, стиль Y2K\n"
        "• `闲置` — личные вещи, обычно дешевле\n"
        "• `断舍离` — расхламление, самые низкие цены\n"
        "• `包邮` — бесплатная доставка по Китаю\n\n"
        "После поиска выбери сортировку `最新发布` (сначала новые)."
    )

@dp.message(F.text == BTN_TEMPLATES)
async def show_templates(message: Message) -> None:
    await message.answer(
        "*Фразы продавцу* (нажми, чтобы скопировать):\n\n"
        "1. Фото бирок и торг:\n"
        "`亲，拍一下里面水洗标和内标的特写呗？如果可以的话，能不能稍微便宜一点，喜欢就直接拍了~`\n\n"
        "2. Упаковка для кепок и сумок:\n"
        "`亲，请用纸箱或者气泡柱帮我包装好一点，别压坏了形状，谢谢！`"
    )

# Микро-сервер для бесплатного тарифного плана Render
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

async def main() -> None:
    logging.info("Бот и веб-сервер запущены")
    await asyncio.gather(
        dp.start_polling(bot),
        web_server()
    )

if __name__ == "__main__":
    asyncio.run(main())
