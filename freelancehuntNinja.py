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
            print(f"🔍 Загружаем проекты для категории {cat}...")
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            print(f"✅ Получено {len(data.get('data', []))} проектов для категории {cat}")
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
    print("⏳ Проверка новых проектов...")
    for cat in CATEGORIES:
        params = {"filter[skill_id]": cat}
        try:
            print(f"🔍 Запрос к категории {cat}...")
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            projects = data.get("data", [])
            print(f"✅ Получено {len(projects)} проектов для категории {cat}")
            for item in projects:
                project_id = item["id"]
                if project_id not in seen_projects:
                    seen_projects.add(project_id)
                    title = item["attributes"]["name"]
                    desc = item["attributes"]["description"][:200] + "..."
                    link = item["links"]["web"]
                    text = f"💼 <b>{title}</b>\n\n{desc}\n\n🔗 {link}"
                    print(f"📤 Отправка проекта {project_id} ({title}) в чат {CHAT_ID}")
                    try:
                        bot.send_message(CHAT_ID, text, parse_mode="HTML")
                        print(f"✅ Успешно отправлено: {title}")
                    except Exception as e:
                        print(f"❌ Ошибка отправки проекта {project_id}: {e}")
        except Exception as e:
            print(f"❌ Ошибка запроса категории {cat}: {e}")
    print("✅ Проверка всех категорий завершена.")

def main():
    print("🚀 Запуск бота...")
    try:
        init_seen_projects()
        print("✅ init_seen_projects завершена")
    except Exception as e:
        print(f"❌ Ошибка в init_seen_projects: {e}")

    try:
        bot.send_message(CHAT_ID, "🚀 Bot запущен и готов мониторить проекты!")
        print("✅ Тестовое сообщение отправлено в чат.")
    except Exception as e:
        print(f"❌ Ошибка отправки тестового сообщения: {e}")

    print("🔄 Входим в цикл проверки каждые 5 минут...")
    while True:
        try:
            check_new_projects()
        except Exception as e:
            print(f"❌ Ошибка в цикле проверки проектов: {e}")
        time.sleep(300)

if __name__ == "__main__":
    main()
