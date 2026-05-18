"""
Облачный Telegram Bot для FreelanceHunt Ninja v3
Хостим на Railway и отправляем команды на локальный Mac сервер.
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

API_TOKEN = os.getenv("7474098596:AAGbmTknoHjMFSMa9zomn_GFUtt0lyGEVDY")
FREELANCEHUNT_TOKEN = os.getenv("dae434aed0d10e2e317db5784e1c9d9e9a1965cc")
CHAT_ID = os.getenv("-1003016177605")
MAC_SERVER_URL = os.getenv("MAC_SERVER_URL")  # URL твоего Mac (через ngrok или постоянный)

bot = telebot.TeleBot(API_TOKEN)

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
    """Генерация отклика - отправляет запрос на Mac сервер."""
    parts = call.data.split("_")
    lang = parts[1].upper()
    project_id = int(parts[2])
    
    bot.answer_callback_query(call.id, f"⏳ Генерую відгук ({lang})...")
    
    # Получаем проект
    project = get_full_project(project_id)
    if not project:
        bot.send_message(CHAT_ID, "❌ Не вдалось отримати проект")
        return
    
    bot.send_message(CHAT_ID, f"🤖 Відправляю запит на Mac...\n<b>{project['title']}</b>", parse_mode="HTML")
    
    # Отправляем запрос на Mac сервер для генерации
    try:
        response = requests.post(
            f"{MAC_SERVER_URL}/webhook/generate",
            json={
                "project_id": project_id,
                "title": project["title"],
                "description": project["description"],
                "lang": lang,
                "callback_url": f"https://ingenious-cooperation-production-5f53.up.railway.app/callback"  # замени на свой URL
            },
            timeout=90
        )
        
        if response.status_code == 200:
            result_data = response.json()
            result = result_data.get("result", {})
            
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
            
            markup = InlineKeyboardMarkup()
            markup.row(
                InlineKeyboardButton("✅ Відправити", callback_data=f"send_{project_id}"),
                InlineKeyboardButton(f"🔄 Ще раз ({lang})", callback_data=f"regen_{lang.lower()}_{project_id}")
            )
            markup.row(
                InlineKeyboardButton("❌ Скасувати", callback_data=f"cancel_{project_id}")
            )
            
            bot.send_message(
                CHAT_ID,
                f"📋 <b>Готовий відгук:</b>\n\n"
                f"{message_text}\n\n"
                f"━━━━━━━━━━━━━━\n"
                f"💰 Ціна: <b>{price_min}-{price_max} грн</b>\n"
                f"⏱ Строки: <b>{days} днів</b>\n"
                f"🎯 Впевненість AI: <b>{confidence}%</b>\n\n"
                f"🔗 <a href='{project['link']}'>Відкрити проект</a>",
                parse_mode="HTML",
                reply_markup=markup,
                disable_web_page_preview=True
            )
        else:
            bot.send_message(CHAT_ID, f"❌ Помилка Mac сервера: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        bot.send_message(
            CHAT_ID,
            "⚠️ <b>Mac сервер недоступний</b>\n\n"
            "Переконайся що:\n"
            "1. Mac увімкнений\n"
            "2. Сервер запущений: <code>python3 mac_server_v3.py</code>\n"
            "3. ngrok працює (якщо потрібен)\n\n"
            f"URL: {MAC_SERVER_URL}",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ Помилка: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith("send_"))
def handle_send(call):
    """Отправка отклика - триггерит OS-level автоматизацию на Mac."""
    global daily_bids, weekly_bids
    
    project_id = int(call.data.split("_")[1])
    
    # Anti-duplicate
    if project_id in sent_bids_today:
        bot.answer_callback_query(call.id, "⚠️ Вже відправляли відгук на цей проект сьогодні")
        return
    
    # Получаем данные
    bid_data = pending_bids.get(project_id)
    if not bid_data:
        bot.answer_callback_query(call.id, "❌ Дані втрачені")
        return
    
    bot.answer_callback_query(call.id, "🚀 Запускаю Mac автоматизацію...")
    
    project = bid_data["project"]
    result = bid_data["result"]
    
    # Отправляем команду на Mac для OS-level автоматизации
    try:
        response = requests.post(
            f"{MAC_SERVER_URL}/webhook/submit",
            json={
                "project_id": project_id,
                "url": project["link"],
                "message": result["message"],
                "days": result["days"],
                "price": result["price_max"],
                "callback_url": f"https://ingenious-cooperation-production-5f53.up.railway.app/callback"
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
            f"URL: {MAC_SERVER_URL}",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ Помилка: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith("regen_"))
def handle_regen(call):
    """Регенерация отклика."""
    parts = call.data.split("_")
    lang = parts[1].upper()
    project_id = int(parts[2])
    
    # Используем ту же логику что и generate
    handle_generate_internal(project_id, lang, call.message)


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


def handle_generate_internal(project_id, lang, message):
    """Внутренняя функция для генерации (для regen)."""
    bid_data = pending_bids.get(project_id)
    if not bid_data:
        bot.send_message(CHAT_ID, "❌ Дані проекту втрачено")
        return
    
    project = bid_data["project"]
    
    try:
        response = requests.post(
            f"{MAC_SERVER_URL}/webhook/generate",
            json={
                "project_id": project_id,
                "title": project["title"],
                "description": project["description"],
                "lang": lang,
                "callback_url": None
            },
            timeout=90
        )
        
        if response.status_code == 200:
            result_data = response.json()
            result = result_data.get("result", {})
            
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
                message.chat.id,
                message.message_id,
                parse_mode="HTML",
                reply_markup=markup,
                disable_web_page_preview=True
            )
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ Помилка: {e}")


# Callback endpoint для статусов от Mac
from flask import Flask, request as flask_request

flask_app = Flask(__name__)

@flask_app.route('/callback', methods=['POST'])
def callback():
    """Принимает статусы от Mac сервера."""
    global daily_bids, weekly_bids
    
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


# Мониторинг проектов
def init_seen_projects():
    """Инициализация."""
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
        except:
            pass
    
    print(f"✅ Завершено. Проектів: {total}")


def check_new_projects():
    """Проверка новых проектов."""
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
                    except:
                        pass
        
        except:
            pass


def scheduler():
    """Главный планировщик."""
    print("🚀 Cloud Telegram Bot v3 запускається...")
    init_seen_projects()
    
    try:
        bot.send_message(
            CHAT_ID,
            "🚀 <b>Ninja v3 запущений!</b>\n\n"
            "☁️ Бот в хмарі (Render/Railway)\n"
            "🖥 Mac сервер для автоматизації\n"
            "🦊 OS-level Firefox automation",
            parse_mode="HTML"
        )
    except:
        pass
    
    # Polling
    polling_thread = threading.Thread(target=bot.polling, kwargs={"none_stop": True})
    polling_thread.daemon = True
    polling_thread.start()
    
    # Monitoring loop
    while True:
        try:
            check_new_projects()
        except:
            pass
        time.sleep(300)


if __name__ == "__main__":
    # Запускаем Flask callback сервер
    flask_thread = threading.Thread(
        target=lambda: flask_app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080))),
        daemon=True
    )
    flask_thread.start()
    
    # Запускаем scheduler
    scheduler()
