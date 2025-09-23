import os
import time
import requests
import telebot
from dotenv import load_dotenv

# Загружаем токены из .env или используем дефолтные
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7474098596:AAGbmTknoHjMFSMa9zomn_GFUtt0lyGEVDY")
FREELANCEHUNT_TOKEN = os.getenv("FREELANCEHUNT_TOKEN", "dae434aed0d10e2e317db5784e1c9d9e9a1965cc")
CHAT_ID = os.getenv("CHAT_ID", "-1003016177605")

bot = telebot.TeleBot(API_TOKEN)

# Категории, которые отслеживаем
CATEGORIES = [99, 78, 175, 124, 43, 129, 68, 96, 134, 14, 183, 120]
seen_projects = set()

def init_seen_projects():
    """Фиксируем существующие проекты при старте, чтобы их не шлать."""
    headers = {"Authorization": f"Bearer {FREELANCEHUNT_TOKEN}"}
    url = "https://api.freelancehunt.com/v2/projects"
    total = 0
    print("🚀 Старт инициализации проектов...")
    for cat in CATEGORIES:
        params = {"filter[skill_id]": cat}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("data", []):
                seen_projects.add(item["id"])
                total += 1
        except Exception as e:
            print(f"❌ Ошибка инициализации категории {cat}: {e}")
    print(f"✅ Инициализация завершена. Всего сохранено проектов: {total}")

def check_new_projects():
    """Проверяем новые проекты и отправляем только появившиеся после запуска."""
    headers = {"Authorization": f"Bearer {FREELANCEHUNT_TOKEN}"}
    url = "https://api.freelancehunt.com/v2/projects"
    for cat in CATEGORIES:
        params = {"filter[skill_id]": cat}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("data", []):
                project_id = item["id"]
                if project_id not in seen_projects:
                    seen_projects.add(project_id)
                    title = item["attributes"]["name"]
                    desc = item["attributes"]["description"][:200] + "..."
                    link = item["links"]["web"]
                    text = f"💼 <b>{title}</b>\n\n{desc}\n\n🔗 {link}"
                    try:
                        bot.send_message(CHAT_ID, text, parse_mode="HTML")
                    except Exception as e:
                        print(f"❌ Ошибка отправки проекта {project_id}: {e}")
        except Exception as e:
            print(f"❌ Ошибка запроса категории {cat}: {e}")

def scheduler():
    print("🚀 Ninja запускается...")
    init_seen_projects()
    try:
        bot.send_message(CHAT_ID, "🚀 Ninja запущен и готов хоботить проекты!")
    except Exception as e:
        print(f"❌ Ошибка отправки тестового сообщения: {e}")

    while True:
        try:
            check_new_projects()
        except Exception as e:
            print(f"❌ Ошибка в цикле проверки проектов: {e}")
        time.sleep(300)  # проверяем каждые 5 минут

if __name__ == "__main__":
    scheduler()
