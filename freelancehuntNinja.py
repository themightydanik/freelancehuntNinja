"""
Telegram Bot для FreelanceHunt Ninja v3
Работает независимо от доступности Mac сервера.
Продолжает мониторить проекты даже если генерация/отправка недоступна.
"""

import os
import time
import random
import threading
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from datetime import datetime
import pytz
import re

load_dotenv()

# Конфигурация
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7474098596:AAGbmTknoHjMFSMa9zomn_GFUtt0lyGEVDY")
FREELANCEHUNT_TOKEN = os.getenv("FREELANCEHUNT_TOKEN", "dae434aed0d10e2e317db5784e1c9d9e9a1965cc")
CHAT_ID = os.getenv("CHAT_ID", "-1003016177605")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Добавь в Railway variables

# Railway URL для Telegram webhook
RAILWAY_URL = os.getenv("RAILWAY_URL", "https://ingenious-cooperation-production-5f53.up.railway.app")

# Mac server URL для отправки команд автоматизации
MAC_SERVER_URL = os.getenv("MAC_SERVER_URL", "http://localhost:3000")

bot = telebot.TeleBot(API_TOKEN)

# Groq client для генерации
from groq import Groq
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

KYIV_TZ = pytz.timezone("Europe/Kiev")
CATEGORIES = [99, 78, 175, 124, 43, 129, 68, 96, 134, 14, 183, 120]

seen_projects = set()
projects_cache = {}
pending_bids = {}
sent_bids_today = set()

# Счётчики
daily_bids = 0
weekly_bids = 0
last_daily_report = None
last_weekly_report = None

# Статус Mac сервера
mac_server_available = False
last_mac_check = 0


# ─── Промпты для генерации ──────────────────────────────────────────────────

SYSTEM_PROMPT_UA = """Ти — досвідчений веб-дизайнер, WordPress розробник і SEO спеціаліст з 10 роками досвіду. Пишеш відгук від імені жінки-фрілансера УКРАЇНСЬКОЮ мовою.

КРИТИЧНО ВАЖЛИВО: Кожен відгук повинен бути АБСОЛЮТНО УНІКАЛЬНИМ за структурою. Думай як senior sales manager.

СТРУКТУРА (з переносами рядків):

Доброго дня[, Ім'я якщо є].

[2-3 речення про розуміння проекту - БЕЗ пересказу заголовка]

Що зроблю:
— [конкретний пункт]
— [конкретний пункт]
— [ще 2-4 пункти]

[Бонус/додаткова цінність]

Строки: [X днів] після отримання матеріалів.

Вартість: [ОДНА КОНКРЕТНА ЦІНА] грн.

Буду рада обговорити деталі.

РОЗРАХУНОК ВАРТОСТІ:
- Почасова ставка: $20/год (≈800 грн/год)
- Оціни реальні години роботи
- У 70% випадків вказуй ОДНУ ціну (середню)
- У 30% випадків можна вказати діапазон якщо проект дуже невизначений

ЗАБОРОНИ:
- НЕ переказуй заголовок проекту
- НЕ повторюй опис проекту
- НЕ згадуй Kolos Agency
- Без emoji
- Тон — впевнений, природній, жіночий

ВАЖЛИВО: Відповідь у форматі JSON:
{
  "message": "текст з переносами рядків \\n\\n",
  "price_min": 3000,
  "price_max": 3000,
  "days": 7,
  "confidence": 0.85
}

Якщо одна ціна: price_min = price_max"""

SYSTEM_PROMPT_RU = """Ты — опытный веб-дизайнер, WordPress разработчик и SEO специалист с 10 годами опыта. Пишешь отклик от имени женщины-фрилансера на РУССКОМ языке.

КРИТИЧЕСКИ ВАЖНО: Каждый отклик должен быть АБСОЛЮТНО УНИКАЛЬНЫМ по структуре. Думай как senior sales manager.

СТРУКТУРА (с переносами строк):

Добрый день[, Имя если есть].

[2-3 предложения о понимании проекта - БЕЗ пересказа заголовка]

Что сделаю:
— [конкретный пункт]
— [конкретный пункт]
— [ещё 2-4 пункта]

[Бонус/дополнительная ценность]

Сроки: [X дней] после получения материалов.

Стоимость: [ОДНА КОНКРЕТНАЯ ЦЕНА] грн.

Буду рада обсудить детали.

РАСЧЁТ СТОИМОСТИ:
- Почасовая ставка: $20/час (≈800 грн/час)
- Оцени реальные часы работы
- В 70% случаев указывай ОДНУ цену (среднюю)
- В 30% случаев можно указать диапазон если проект очень неопределённый

ЗАПРЕТЫ:
- НЕ пересказывай заголовок проекта
- НЕ повторяй описание проекта
- НЕ упоминай Kolos Agency
- Без emoji
- Тон — уверенный, естественный, женский

ВАЖНО: Ответ в формате JSON:
{
  "message": "текст с переносами строк \\n\\n",
  "price_min": 3000,
  "price_max": 3000,
  "days": 7,
  "confidence": 0.85
}

Если одна цена: price_min = price_max"""


def generate_response_groq(title: str, description: str, lang: str = "UA", budget: dict = None) -> dict:
    """
    Генерирует отклик через Groq API.
    Работает прямо в Railway - быстро и надежно.
    """
    if not groq_client:
        return {
            "message": "❌ GROQ_API_KEY не настроен",
            "price_min": 0,
            "price_max": 0,
            "days": 0,
            "confidence": 0
        }
    
    system_prompt = SYSTEM_PROMPT_UA if lang == "UA" else SYSTEM_PROMPT_RU
    
    budget_info = ""
    if budget and budget.get("amount"):
        budget_info = f"\nБюджет клиента: {budget['amount']} {budget.get('currency', 'UAH')}"
    
    user_prompt = f"""Назва проекту: {title}

Опис: {description}{budget_info}

Створи УНІКАЛЬНИЙ відгук. Проаналізуй складність, запропонуй реалістичну ціну (2000-20000 грн) і строки (3-21 днів).

Відповідь СТРОГО у форматі JSON (без markdown, без пояснень):
{{
  "message": "текст",
  "price_min": число,
  "price_max": число,
  "days": число,
  "confidence": 0.0-1.0
}}"""

    try:
        response = groq_client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2250,
            temperature=0.69
        )
        
        text = response.choices[0].message.content
        
        # Парсим JSON
        import json
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group(0))
            if "message" in parsed:
                return {
                    "message": parsed.get("message", text),
                    "price_min": max(1000, min(parsed.get("price_min", 3000), 50000)),
                    "price_max": max(1000, min(parsed.get("price_max", 5000), 50000)),
                    "days": max(1, min(parsed.get("days", 7), 30)),
                    "confidence": max(0, min(parsed.get("confidence", 0.75), 1))
                }
        
        # Fallback
        return {
            "message": text,
            "price_min": 3000,
            "price_max": 5000,
            "days": 7,
            "confidence": 0.5
        }
        
    except Exception as e:
        print(f"❌ Groq error: {e}")
        return {
            "message": f"❌ Помилка генерації: {str(e)}",
            "price_min": 0,
            "price_max": 0,
            "days": 0,
            "confidence": 0
        }


def check_mac_server():
    """
    Проверяет доступность Mac сервера.
    Не падает если сервер недоступен.
    """
    global mac_server_available, last_mac_check
    
    # Проверяем не чаще раза в минуту
    now = time.time()
    if now - last_mac_check < 60:
        return mac_server_available
    
    last_mac_check = now
    
    try:
        response = requests.get(f"{MAC_SERVER_URL}/health", timeout=3)
        mac_server_available = response.status_code == 200
        return mac_server_available
    except:
        mac_server_available = False
        return False


def title_to_slug(title: str) -> str:
    """Конвертирует заголовок в URL slug."""
    translit = {
        'а':'a','б':'b','в':'v','г':'g','ґ':'g','д':'d','е':'e','є':'ye',
        'ж':'zh','з':'z','и':'i','і':'i','ї':'yi','й':'y','к':'k','л':'l',
        'м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u',
        'ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch','ь':'',
        'ю':'yu','я':'ya','ё':'yo','ъ':'','ы':'y','э':'e',
    }
    slug = title.lower()
    result = ''
    for ch in slug:
        result += translit.get(ch, ch)
    result = re.sub(r'[^a-z0-9\s-]', '', result)
    result = re.sub(r'[\s]+', '-', result.strip())
    result = re.sub(r'-+', '-', result)
    return result[:80]


def get_full_project(project_id: int) -> dict:
    """Получает полную информацию о проекте."""
    headers = {"Authorization": f"Bearer {FREELANCEHUNT_TOKEN}"}
    url = f"https://api.freelancehunt.com/v2/projects/{project_id}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        attrs = data.get("data", {}).get("attributes", {})
        links = data.get("data", {}).get("links", {})
        
        title = attrs.get("name", "")
        link = links.get("web") or f"https://freelancehunt.com/project/{title_to_slug(title)}/{project_id}.html"
        
        return {
            "title": title,
            "description": attrs.get("description", ""),
            "link": link,
            "budget": attrs.get("budget", {})
        }
    except Exception as e:
        print(f"❌ Ошибка получения проекта {project_id}: {e}")
        return {}


@bot.callback_query_handler(func=lambda call: call.data.startswith("generate_"))
def handle_generate(call):
    """
    Генерация отклика - теперь прямо здесь через Groq API.
    Mac не нужен для генерации.
    """
    parts = call.data.split("_")
    lang = parts[1].upper()
    project_id = int(parts[2])
    
    bot.answer_callback_query(call.id, f"⏳ Генерую відгук ({lang})...")
    
    # Получаем проект
    project = get_full_project(project_id)
    if not project:
        bot.send_message(CHAT_ID, "❌ Не вдалось отримати проект")
        return
    
    bot.send_message(CHAT_ID, f"🤖 Генерую відгук через Groq AI...\n<b>{project['title']}</b>", parse_mode="HTML")
    
    # Генерируем прямо здесь в Railway
    result = generate_response_groq(
        title=project["title"],
        description=project["description"],
        lang=lang,
        budget=project.get("budget")
    )
    
    if result["confidence"] == 0:
        bot.send_message(CHAT_ID, result["message"])  # Ошибка
        return
    
    # Сохраняем для подтверждения
    pending_bids[project_id] = {
        "project": project,
        "result": result,
        "lang": lang
    }
    
    # Формируем сообщение
    message_text = result.get("message", "Ошибка генерации")
    price_min = result.get("price_min", 0)
    price_max = result.get("price_max", 0)
    days = result.get("days", 7)
    confidence = int(result.get("confidence", 0) * 100)
    
    # Форматируем цену (одна или диапазон)
    if price_min == price_max:
        price_str = f"<b>{price_min} грн</b>"
    else:
        price_str = f"<b>{price_min}-{price_max} грн</b>"
    
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Відправити", callback_data=f"send_{project_id}"),
        InlineKeyboardButton(f"🔄 Ще раз ({lang})", callback_data=f"regen_{lang.lower()}_{project_id}")
    )
    markup.row(
        InlineKeyboardButton("✏️ Редагувати", callback_data=f"edit_{project_id}"),
        InlineKeyboardButton("❌ Скасувати", callback_data=f"cancel_{project_id}")
    )
    
    bot.send_message(
        CHAT_ID,
        f"📋 <b>Готовий відгук:</b>\n\n"
        f"{message_text}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"💰 Ціна: {price_str}\n"
        f"⏱ Строки: <b>{days} днів</b>\n"
        f"🎯 Впевненість AI: <b>{confidence}%</b>\n\n"
        f"🔗 <a href='{project['link']}'>Відкрити проект</a>",
        parse_mode="HTML",
        reply_markup=markup,
        disable_web_page_preview=True
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("send_"))
def handle_send(call):
    """
    Отправка отклика - триггерит автоматизацию на Mac.
    Mac получает готовые данные (текст, цену, сроки).
    """
    global daily_bids, weekly_bids
    
    project_id = int(call.data.split("_")[1])
    
    # Проверяем доступность Mac сервера
    if not check_mac_server():
        bot.answer_callback_query(
            call.id,
            "⚠️ Mac сервер недоступний. Запусти локально.",
            show_alert=True
        )
        bot.send_message(
            CHAT_ID,
            "⚠️ <b>Mac сервер недоступний</b>\n\n"
            "Запусти на Mac:\n"
            "1. <code>python3 mac_server_v3.py</code>\n"
            "2. <code>ngrok http 3000</code>\n"
            "3. Оновіть MAC_SERVER_URL в Railway\n\n"
            f"Поточний URL: <code>{MAC_SERVER_URL}</code>",
            parse_mode="HTML"
        )
        return
    
    # Anti-duplicate
    if project_id in sent_bids_today:
        bot.answer_callback_query(call.id, "⚠️ Вже відправляли відгук на цей проект сьогодні")
        return
    
    # Получаем данные
    bid_data = pending_bids.get(project_id)
    if not bid_data:
        bot.answer_callback_query(call.id, "❌ Дані втрачені")
        return
    
    bot.answer_callback_query(call.id, "🚀 Запускаю автоматизацію...")
    
    project = bid_data["project"]
    result = bid_data["result"]
    
    # Отправляем команду на Mac - только готовые данные для автоматизации
    try:
        response = requests.post(
            f"{MAC_SERVER_URL}/webhook/submit",
            json={
                "project_id": project_id,
                "url": project["link"],
                "message": result["message"],
                "days": result["days"],
                "price": result["price_max"]
            },
            timeout=10
        )
        
        if response.status_code == 200:
            sent_bids_today.add(project_id)
            
            bot.send_message(
                CHAT_ID,
                f"⏳ <b>Автоматизація запущена на Mac</b>\n\n"
                f"Firefox відкриється автоматично і відправить відгук.\n"
                f"Отримаєш повідомлення після завершення.",
                parse_mode="HTML"
            )
            
            # Удаляем из pending
            del pending_bids[project_id]
            
        else:
            bot.send_message(CHAT_ID, f"❌ Помилка Mac сервера: {response.text}")
            
    except requests.exceptions.ConnectionError:
        bot.send_message(
            CHAT_ID,
            "⚠️ <b>Mac сервер недоступний</b>\n\n"
            "Відгук НЕ відправлено. Запусти Mac сервер.",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ Помилка: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith("regen_"))
def handle_regen(call):
    """Регенерация отклика через Groq."""
    parts = call.data.split("_")
    lang = parts[1].upper()
    project_id = int(parts[2])
    
    bot.answer_callback_query(call.id, "🔄 Перегенеровую...")
    
    bid_data = pending_bids.get(project_id)
    if not bid_data:
        bot.send_message(CHAT_ID, "❌ Дані проекту втрачено")
        return
    
    project = bid_data["project"]
    
    # Генерируем заново через Groq
    result = generate_response_groq(
        title=project["title"],
        description=project["description"],
        lang=lang,
        budget=project.get("budget")
    )
    
    if result["confidence"] == 0:
        bot.send_message(CHAT_ID, result["message"])
        return
    
    # Обновляем данные
    pending_bids[project_id]["result"] = result
    pending_bids[project_id]["lang"] = lang
    
    message_text = result.get("message", "")
    price_min = result.get("price_min", 0)
    price_max = result.get("price_max", 0)
    days = result.get("days", 7)
    confidence = int(result.get("confidence", 0) * 100)
    
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ Відправити", callback_data=f"send_{project_id}"),
        InlineKeyboardButton(f"🔄 Ще раз ({lang})", callback_data=f"regen_{lang.lower()}_{project_id}")
    )
    markup.row(
        InlineKeyboardButton("❌ Скасувати", callback_data=f"cancel_{project_id}")
    )
    
    bot.edit_message_text(
        f"📋 <b>Новий відгук:</b>\n\n"
        f"{message_text}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"💰 Ціна: <b>{price_min}-{price_max} грн</b>\n"
        f"⏱ Строки: <b>{days} днів</b>\n"
        f"🎯 Впевненість AI: <b>{confidence}%</b>\n\n"
        f"🔗 <a href='{project['link']}'>Відкрити проект</a>",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup,
        disable_web_page_preview=True
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("cancel_"))
def handle_cancel(call):
    """Отмена."""
    project_id = int(call.data.split("_")[1])
    
    if project_id in pending_bids:
        del pending_bids[project_id]
    
    bot.answer_callback_query(call.id, "Скасовано")
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("skip_"))
def handle_skip(call):
    """Пропуск проекта."""
    bot.answer_callback_query(call.id, "Пропущено")
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )


# ─── Callback endpoint для статусов от Mac ──────────────────────────────────
from flask import Flask, request as flask_request

flask_app = Flask(__name__)

@flask_app.route('/callback', methods=['POST'])
def callback():
    """Принимает статусы от Mac сервера."""
    global daily_bids, weekly_bids
    
    try:
        data = flask_request.json
        project_id = data.get("project_id")
        status = data.get("status")
        message = data.get("message")
        
        if status == "success":
            daily_bids += 1
            weekly_bids += 1
            
            bot.send_message(
                CHAT_ID,
                f"✅ <b>Відгук відправлено!</b>\n\n"
                f"📊 Сьогодні: <b>{daily_bids}</b> | За тиждень: <b>{weekly_bids}</b>",
                parse_mode="HTML"
            )
        elif status == "failed" or status == "error":
            bot.send_message(
                CHAT_ID,
                f"❌ <b>Помилка відправки</b>\n\n"
                f"{message or 'Невідома помилка'}",
                parse_mode="HTML"
            )
        elif status == "processing":
            # Опционально - можно отправить статус
            pass
        
        return {"status": "ok"}, 200
    except Exception as e:
        print(f"❌ Callback error: {e}")
        return {"status": "error", "message": str(e)}, 500


# Мониторинг проектов
def init_seen_projects():
    """
    Инициализация.
    Работает независимо от Mac сервера.
    """
    headers = {"Authorization": f"Bearer {FREELANCEHUNT_TOKEN}"}
    url = "https://api.freelancehunt.com/v2/projects"
    total = 0
    print("🚀 Ініціалізація проектів...")
    
    for cat in CATEGORIES:
        params = {"filter[skill_id]": cat}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            for item in resp.json().get("data", []):
                seen_projects.add(item["id"])
                total += 1
        except Exception as e:
            print(f"⚠️ Помилка категорії {cat}: {e}")
            continue
    
    print(f"✅ Завершено. Проектів: {total}")


def check_new_projects():
    """
    Проверка новых проектов.
    Работает независимо от Mac сервера - только мониторинг Freelancehunt.
    """
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
                    link = links.get("web") or f"https://freelancehunt.com/project/{title_to_slug(title)}/{project_id}.html"
                    
                    projects_cache[project_id] = {
                        "title": title,
                        "description": description,
                        "link": link
                    }
                    
                    markup = InlineKeyboardMarkup()
                    markup.row(
                        InlineKeyboardButton("🇺🇦 Генерувати UA", callback_data=f"generate_ua_{project_id}"),
                        InlineKeyboardButton("🇷🇺 Генерувати RU", callback_data=f"generate_ru_{project_id}")
                    )
                    markup.row(
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
                        print(f"⚠️ Помилка відправки проекту {project_id}: {e}")
        
        except Exception as e:
            print(f"⚠️ Помилка категорії {cat}: {e}")
            continue


def projects_monitor():
    """
    Фоновый мониторинг проектов.
    Работает в отдельном потоке.
    """
    print("🔍 Мониторинг проектів запущено")
    
    while True:
        try:
            check_new_projects()
        except Exception as e:
            print(f"⚠️ Помилка моніторингу: {e}")
        time.sleep(300)  # каждые 5 минут


@flask_app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    """
    Webhook endpoint для Telegram.
    Принимает обновления от Telegram вместо polling.
    """
    try:
        json_string = flask_request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return '', 500


def setup_webhook():
    """
    Настраивает webhook для Telegram.
    Вызывается один раз при старте.
    """
    try:
        # Удаляем старый webhook/polling
        bot.remove_webhook()
        time.sleep(1)
        
        # Устанавливаем новый webhook
        webhook_url = f"{RAILWAY_URL}/{API_TOKEN}"
        bot.set_webhook(url=webhook_url)
        
        print(f"✅ Webhook установлен: {webhook_url}")
        return True
    except Exception as e:
        print(f"❌ Ошибка установки webhook: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("FREELANCEHUNT NINJA v3 - CLOUD BOT")
    print("="*60)
    print("Webhook mode (stable for Railway)")
    print("="*60 + "\n")
    
    print("🚀 Cloud Telegram Bot v3 запускається...")
    print(f"📡 Freelancehunt API: активний")
    print(f"🖥 Mac Server: {MAC_SERVER_URL}")
    
    # Проверяем Mac сервер при старте
    mac_status = "✅ підключений" if check_mac_server() else "⚠️ недоступний"
    print(f"🔌 Mac Server: {mac_status}")
    
    # Инициализация
    init_seen_projects()
    
    # Запускаем мониторинг проектов в фоне
    monitor_thread = threading.Thread(target=projects_monitor, daemon=True)
    monitor_thread.start()
    
    # Настраиваем webhook
    webhook_ok = setup_webhook()
    
    # Отправляем статус в Telegram
    try:
        status_msg = (
            "🚀 <b>Ninja v3 запущений!</b>\n\n"
            "☁️ Бот в хмарі (Railway)\n"
            "📡 Мониторинг проектів: <b>активний</b>\n"
        )
        
        if webhook_ok:
            status_msg += "🔗 Webhook: <b>активний</b>\n"
        else:
            status_msg += "⚠️ Webhook: <b>помилка налаштування</b>\n"
        
        if mac_server_available:
            status_msg += "🖥 Mac сервер: <b>підключений</b>\n"
            status_msg += "🦊 OS-level automation: <b>готовий</b>"
        else:
            status_msg += "⚠️ Mac сервер: <b>недоступний</b>\n"
            status_msg += "Проекти надходять в Telegram.\n"
            status_msg += "Генерація запрацює після підключення Mac."
        
        bot.send_message(CHAT_ID, status_msg, parse_mode="HTML")
    except Exception as e:
        print(f"⚠️ Помилка відправки статусу: {e}")
    
    # Запускаем Flask (blocking)
    # Это единственный запущенный процесс - никаких конфликтов
    print("🌐 Запускаю Flask webhook server...")
    flask_app.run(
        host='0.0.0.0',
        port=int(os.getenv("PORT", 8080)),
        debug=False,
        use_reloader=False  # ВАЖНО: отключаем reloader чтобы не было дублей
    )
