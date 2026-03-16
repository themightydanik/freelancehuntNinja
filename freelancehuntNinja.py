import os
import time
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7474098596:AAGbmTknoHjMFSMa9zomn_GFUtt0lyGEVDY")
FREELANCEHUNT_TOKEN = os.getenv("FREELANCEHUNT_TOKEN", "dae434aed0d10e2e317db5784e1c9d9e9a1965cc")
CHAT_ID = os.getenv("CHAT_ID", "-1003016177605")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

bot = telebot.TeleBot(API_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("gemini-2.0-flash")

CATEGORIES = [99, 78, 175, 124, 43, 129, 68, 96, 134, 14, 183, 120]
seen_projects = set()
projects_cache = {}

# ─── Промпты ─────────────────────────────────────────────────────────────────

SYSTEM_PROMPT_UA = """Ти — досвідчений веб-дизайнер, WordPress розробник і SEO спеціаліст з 10 роками досвіду.
Твоє агентство — Kolos Agency. Пишеш відгук УКРАЇНСЬКОЮ мовою.

Правила відгуку:
- Максимум 5-6 речень, без води
- Перше речення — одразу про суть проекту, покажи що зрозумів задачу
- Одне речення про релевантний досвід (конкретно, без "я досвідчений фахівець")
- Одне речення про результат який отримає клієнт
- Одне уточнююче питання про проект
- Ніяких шаблонних фраз типу "Здравствуйте! Готов взяться за ваш проект"
- Без зайвих emoji
- Тон — впевнений, дружній, професійний"""

SYSTEM_PROMPT_RU = """Ты — опытный веб-дизайнер, WordPress разработчик и SEO специалист с 10 годами опыта.
Твоё агентство — Kolos Agency. Пишешь отклик на РУССКОМ языке.

Правила отклика:
- Максимум 5-6 предложений, без воды
- Первое предложение — сразу по сути проекта, покажи что понял задачу
- Одно предложение про релевантный опыт (конкретно, без "я опытный специалист")
- Одно предложение про результат который получит клиент
- Один уточняющий вопрос про проект
- Никаких шаблонных фраз типа "Здравствуйте! Готов взяться за ваш проект"
- Без лишних emoji
- Тон — уверенный, дружелюбный, профессиональный"""


# ─── Получение полного описания проекта ──────────────────────────────────────

def get_full_project(project_id: int) -> dict:
    headers = {"Authorization": f"Bearer {FREELANCEHUNT_TOKEN}"}
    url = f"https://api.freelancehunt.com/v2/projects/{project_id}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        attrs = data.get("data", {}).get("attributes", {})
        links = data.get("data", {}).get("links", {})
        return {
            "title": attrs.get("name", ""),
            "description": attrs.get("description", ""),
            "link": links.get("web", f"https://freelancehunt.com/project/{project_id}.html")
        }
    except Exception as e:
        print(f"❌ Помилка отримання проекту {project_id}: {e}")
        return {}


# ─── Генерация отклика через Gemini ──────────────────────────────────────────

def generate_response(title: str, description: str, lang: str = "UA") -> str:
    system_prompt = SYSTEM_PROMPT_UA if lang == "UA" else SYSTEM_PROMPT_RU
    prompt = f"{system_prompt}\n\nНазва проекту: {title}\n\nОпис: {description}"
    try:
        response = gemini.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Помилка генерації: {e}"


# ─── Обработчики кнопок ──────────────────────────────────────────────────────

@bot.callback_query_handler(func=lambda call: call.data.startswith("respond_ua_") or call.data.startswith("respond_ru_"))
def handle_respond(call):
    parts = call.data.split("_")
    lang = parts[1].upper()
    project_id = int(parts[2])

    bot.answer_callback_query(call.id, f"⏳ Генерую відгук ({lang})...")

    project = get_full_project(project_id)
    if not project:
        bot.send_message(CHAT_ID, "❌ Не вдалось отримати дані проекту")
        return

    title = project["title"]
    description = project["description"]
    link = project["link"]

    projects_cache[project_id] = {
        "title": title,
        "description": description,
        "link": link
    }

    lang_label = "🇺🇦 UA" if lang == "UA" else "🇷🇺 RU"
    bot.send_message(CHAT_ID, f"✍️ Генерую відгук {lang_label} для:\n<b>{title}</b>", parse_mode="HTML")

    response_text = generate_response(title, description, lang)
    projects_cache[project_id]["generated_response"] = response_text

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(f"🔄 Ще раз ({lang})", callback_data=f"regen_{lang.lower()}_{project_id}"),
        InlineKeyboardButton("❌ Скасувати", callback_data=f"cancel_{project_id}")
    )

    bot.send_message(
        CHAT_ID,
        f"📋 <b>Скопіюй і встав відгук:</b>\n\n{response_text}\n\n🔗 <a href='{link}'>Відкрити проект</a>",
        parse_mode="HTML",
        reply_markup=markup,
        disable_web_page_preview=True
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("regen_"))
def handle_regen(call):
    parts = call.data.split("_")
    lang = parts[1].upper()
    project_id = int(parts[2])

    bot.answer_callback_query(call.id, "🔄 Перегенеровую...")

    project = get_full_project(project_id)
    if not project:
        bot.send_message(CHAT_ID, "❌ Не вдалось отримати дані проекту")
        return

    response_text = generate_response(project["title"], project["description"], lang)
    projects_cache[project_id]["generated_response"] = response_text

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(f"🔄 Ще раз ({lang})", callback_data=f"regen_{lang.lower()}_{project_id}"),
        InlineKeyboardButton("❌ Скасувати", callback_data=f"cancel_{project_id}")
    )

    bot.edit_message_text(
        f"📋 <b>Новий відгук — скопіюй і встав:</b>\n\n{response_text}\n\n🔗 <a href='{project['link']}'>Відкрити проект</a>",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup,
        disable_web_page_preview=True
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("cancel_"))
def handle_cancel(call):
    bot.answer_callback_query(call.id, "Скасовано")
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("skip_"))
def handle_skip(call):
    bot.answer_callback_query(call.id, "Пропущено")
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )


# ─── Мониторинг новых проектов ────────────────────────────────────────────────

def init_seen_projects():
    headers = {"Authorization": f"Bearer {FREELANCEHUNT_TOKEN}"}
    url = "https://api.freelancehunt.com/v2/projects"
    total = 0
    print("🚀 Старт ініціалізації проектів...")
    for cat in CATEGORIES:
        params = {"filter[skill_id]": cat}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            for item in resp.json().get("data", []):
                seen_projects.add(item["id"])
                total += 1
        except Exception as e:
            print(f"❌ Помилка ініціалізації категорії {cat}: {e}")
    print(f"✅ Ініціалізація завершена. Збережено проектів: {total}")


def check_new_projects():
    headers = {"Authorization": f"Bearer {FREELANCEHUNT_TOKEN}"}
    url = "https://api.freelancehunt.com/v2/projects"

    for cat in CATEGORIES:
        params = {"filter[skill_id]": cat}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()

            for item in resp.json().get("data", []):
                project_id = item["id"]
                if project_id not in seen_projects:
                    seen_projects.add(project_id)

                    attrs = item["attributes"]
                    title = attrs.get("name", "Без назви")
                    description = attrs.get("description", "")

                    budget_info = attrs.get("budget", {})
                    budget_str = ""
                    if budget_info and budget_info.get("amount"):
                        budget_str = f"\n💰 Бюджет: {budget_info['amount']} {budget_info.get('currency', '')}"

                    links = item.get("links", {})
                    link = links.get("web") or f"https://freelancehunt.com/project/{project_id}.html"

                    projects_cache[project_id] = {
                        "title": title,
                        "description": description,
                        "link": link
                    }

                    markup = InlineKeyboardMarkup()
                    markup.row(
                        InlineKeyboardButton("🇺🇦 Відгук UA", callback_data=f"respond_ua_{project_id}"),
                        InlineKeyboardButton("🇷🇺 Відгук RU", callback_data=f"respond_ru_{project_id}"),
                        InlineKeyboardButton("❌ Пропустити", callback_data=f"skip_{project_id}")
                    )

                    short_desc = description[:300] + "..." if len(description) > 300 else description
                    text = (
                        f"💼 <b>{title}</b>{budget_str}\n\n"
                        f"{short_desc}\n\n"
                        f"🔗 <a href='{link}'>Відкрити проект</a>"
                    )

                    try:
                        bot.send_message(
                            CHAT_ID, text,
                            parse_mode="HTML",
                            reply_markup=markup,
                            disable_web_page_preview=True
                        )
                    except Exception as e:
                        print(f"❌ Помилка відправки {project_id}: {e}")

        except Exception as e:
            print(f"❌ Помилка категорії {cat}: {e}")


def scheduler():
    import threading

    print("🚀 Ninja запускається...")
    init_seen_projects()

    try:
        bot.send_message(CHAT_ID, "🚀 Ninja запущений! Gemini AI готовий 🤖\nОбирай мову і копіюй текст 📋")
    except Exception as e:
        print(f"❌ Помилка старту: {e}")

    polling_thread = threading.Thread(target=bot.polling, kwargs={"none_stop": True})
    polling_thread.daemon = True
    polling_thread.start()

    while True:
        try:
            check_new_projects()
        except Exception as e:
            print(f"❌ Помилка в циклі: {e}")
        time.sleep(300)


if __name__ == "__main__":
    scheduler()
