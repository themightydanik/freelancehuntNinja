import os
import asyncio
import requests
from aiogram import Bot
from flask import Flask

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7474098596:AAGbmTknoHjMFSMa9zomn_GFUtt0lyGEVDY")
FREELANCEHUNT_TOKEN = os.getenv("FREELANCEHUNT_TOKEN", "dae434aed0d10e2e317db5784e1c9d9e9a1965cc")
CHAT_ID = os.getenv("CHAT_ID", "@freelancehuntninja")  # или числовой ID канала, если приватный

bot = Bot(token=API_TOKEN)

CATEGORIES = [99, 78, 175, 124, 43, 129, 68, 96, 134, 14, 183, 120]
seen_projects = set()

async def init_seen_projects():
    """Фиксируем существующие проекты при старте, чтобы их не шлать."""
    headers = {"Authorization": f"Bearer {FREELANCEHUNT_TOKEN}"}
    url = "https://api.freelancehunt.com/v2/projects"

    for cat in CATEGORIES:
        params = {"filter[skill_id]": cat}
        try:
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("data", []):
                seen_projects.add(item["id"])
        except Exception as e:
            print(f"Ошибка инициализации категории {cat}: {e}")

async def check_new_projects():
    """Проверяем новые проекты и отправляем только появившиеся после запуска."""
    headers = {"Authorization": f"Bearer {FREELANCEHUNT_TOKEN}"}
    url = "https://api.freelancehunt.com/v2/projects"

    for cat in CATEGORIES:
        params = {"filter[skill_id]": cat}
        try:
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()

            for item in data.get("data", []):
                project_id = item["id"]
                if project_id not in seen_projects:
                    seen_projects.add(project_id)

                    title = item["attributes"]["name"]
                    desc = item["attributes"]["description"][:200] + "..."
                    link = item["links"]["web"]  # используем web, чтобы не показывать API

                    text = f"💼 <b>{title}</b>\n\n{desc}\n\n🔗 {link}"
                    await bot.send_message(CHAT_ID, text, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка проверки категории {cat}: {e}")

async def scheduler():
    await init_seen_projects()
    print("Инициализация завершена. Проверяем новые проекты каждые 5 минут.")
    while True:
        try:
            await check_new_projects()
        except Exception as e:
            print(f"Ошибка в цикле проверки проектов: {e}")
        await asyncio.sleep(300)

# Создаём Flask-сервер для Render
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    # Запускаем scheduler в фоне
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())

    # Запускаем Flask для порта
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
