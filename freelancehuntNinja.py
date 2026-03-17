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
from groq import Groq
import re
import unicodedata

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7474098596:AAGbmTknoHjMFSMa9zomn_GFUtt0lyGEVDY")
FREELANCEHUNT_TOKEN = os.getenv("FREELANCEHUNT_TOKEN", "dae434aed0d10e2e317db5784e1c9d9e9a1965cc")
CHAT_ID = os.getenv("CHAT_ID", "-1003016177605")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

bot = telebot.TeleBot(API_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)


KYIV_TZ = pytz.timezone("Europe/Kiev")
CATEGORIES = [99, 78, 175, 124, 43, 129, 68, 96, 134, 14, 183, 120]



# ─── Генерація slug з заголовку ──────────────────────────────────────────────

def title_to_slug(title: str) -> str:
    """Converts project title to URL slug like Freelancehunt does."""
    # Transliteration map for Ukrainian/Russian
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
    # Keep only alphanumeric and hyphens
    result = re.sub(r'[^a-z0-9\s-]', '', result)
    result = re.sub(r'[\s]+', '-', result.strip())
    result = re.sub(r'-+', '-', result)
    return result[:80]

seen_projects = set()
projects_cache = {}

# Счётчики откликов
daily_bids = 0       # сбрасывается каждый день в 23:00
weekly_bids = 0      # сбрасывается каждый понедельник в 09:00
last_daily_report = None
last_weekly_report = None


# ─── Промпты для генерации откликов ──────────────────────────────────────────

SYSTEM_PROMPT_UA = """Ти — досвідчений веб-дизайнер, WordPress розробник і SEO спеціаліст з 10 роками досвіду. Пишеш відгук від імені жінки-фрілансера УКРАЇНСЬКОЮ мовою.

СТРОГО дотримуйся цієї структури і формату — без відступів від неї:

Доброго дня[, Ім'я якщо є в описі проекту].

[2-3 речення: Конкретно що ти можеш зробити для ЦЬОГО проекту. Покажи що зрозуміла задачу. Говори про їхній конкретний проект.]

Що зроблю:
— [конкретний пункт роботи]
— [конкретний пункт роботи]
— [ще 3-6 пунктів залежно від обсягу проекту]

[1 речення — бонус що підвищує цінність. Наприклад: "Після запуску покажу, як самостійно редагувати будь-яку інформацію на сайті." Або інший релевантний бонус. Якщо проект дуже великий — можна згадати що є невелика команда.]

По строках: [X–Y днів] після отримання матеріалів.

Вартість: [X – Y грн] (залежить від [конкретний фактор]).

Буду рада обговорити деталі.

Правила:
- НЕ згадуй Kolos Agency
- Без emoji
- Тон — впевнений, теплий, жіночий
- Якщо імені клієнта немає — просто "Доброго дня." без імені
- Вартість вказуй в гривнях, реалістично для українського ринку"""

SYSTEM_PROMPT_RU = """Ты — опытный веб-дизайнер, WordPress разработчик и SEO специалист с 10 годами опыта. Пишешь отклик от имени женщины-фрилансера на РУССКОМ языке.

СТРОГО соблюдай эту структуру и формат — без отступлений:

Добрый день[, Имя если есть в описании проекта].

[2-3 предложения: Конкретно что ты можешь сделать для ЭТОГО проекта. Покажи что поняла задачу. Говори об их конкретном проекте.]

Что сделаю:
— [конкретный пункт работы]
— [конкретный пункт работы]
— [ещё 3-6 пунктов в зависимости от объёма проекта]

[1 предложение — бонус повышающий ценность. Например: "После запуска покажу, как самостоятельно редактировать любую информацию на сайте." Или другой релевантный бонус. Если проект очень большой — можно упомянуть что есть небольшая команда.]

По срокам: [X–Y дней] после получения материалов.

Стоимость: [X – Y грн] (зависит от [конкретный фактор]).

Буду рада обсудить детали.

Правила:
- НЕ упоминай Kolos Agency
- Без emoji
- Тон — уверенный, тёплый, женский
- Если имени клиента нет — просто "Добрый день." без имени
- Стоимость указывай в гривнях, реалистично для украинского рынка"""



# ─── Цитаты по уровню результата ─────────────────────────────────────────────

QUOTES_LOW = [
    "«Успех — это движение от неудачи к неудаче без потери энтузиазма.» — Уинстон Черчилль",
    "«Неважно, как медленно ты идёшь, главное — не останавливаться.» — Конфуций",
    "«Каждое утро — это новый шанс стать лучше, чем вчера.»",
    "«Даже самый длинный путь начинается с одного шага.» — Лао-цзы",
    "«Трудности — это не причина сдаться, а повод собраться.»",
    "«Человек, который двигается вперёд хотя бы на сантиметр — уже обгоняет тех, кто стоит.»",
]

QUOTES_OK = [
    "«Дисциплина — это мост между целями и достижениями.» — Джим Рон",
    "«Стабильность — это не скучно. Это фундамент.»",
    "«Делай сегодня то, что другие не хотят — завтра будешь жить так, как другие не могут.»",
    "«Последовательность важнее интенсивности. Каждый день понемногу — это и есть система.»",
    "«Богатство — это не удача. Это привычка работать тогда, когда не хочется.»",
    "«Результат — это просто сумма правильных действий, повторённых достаточно много раз.»",
]

QUOTES_HIGH = [
    "«Успех — это не финальная точка. Это стиль жизни.»",
    "«Те, кто говорят, что это невозможно, не должны мешать тем, кто это делает.» — Конфуций",
    "«Если тебе нравится то, что ты делаешь — ты никогда не будешь работать ни дня.» — Конфуций",
    "«Большие дела делаются не силой, а настойчивостью.» — Сэмюэл Джонсон",
    "«Победители делают то, что проигравшие не хотят делать.»",
    "«Деньги — это просто благодарность мира за твою ценность.»",
]


# ─── Формирование дневного отчёта ────────────────────────────────────────────

def get_daily_report(count: int) -> str:
    if count < 5:
        grade = "😐 Маловато, треба піднажати"
        mood = "low"
    elif count == 5:
        grade = "✅ Хороший результат, ми в порядку"
        mood = "ok"
    else:
        grade = "🔥 Бро, ти відриваєшся! Сьогодні прям у вударі!"
        mood = "high"

    if mood == "low":
        quote = random.choice(QUOTES_LOW)
    elif mood == "ok":
        quote = random.choice(QUOTES_OK)
    else:
        quote = random.choice(QUOTES_HIGH)

    return (
        f"📊 <b>Підсумок дня</b>\n\n"
        f"Відгуків відправлено: <b>{count}</b>\n"
        f"Оцінка: {grade}\n\n"
        f"💬 <i>{quote}</i>"
    )


# ─── Формирование недельного отчёта ──────────────────────────────────────────

def get_weekly_report(count: int) -> str:
    if count < 35:
        grade = "😬 Нижче норми. Кріпимо булки і беремося за справу!"
    elif count == 35:
        grade = "💪 Супер, ми в порядку! Рівно по плану."
    else:
        grade = "🚀 Це був вогненний тиждень! Продовжуй — і будемо натирати на бутерброди золоті злитки 🥇"

    return (
        f"📅 <b>Підсумок тижня</b>\n\n"
        f"Відгуків за тиждень: <b>{count}</b>\n"
        f"Ціль: 35 відгуків\n\n"
        f"{grade}"
    )


# ─── Планировщик отчётов ─────────────────────────────────────────────────────

def reports_scheduler():
    global daily_bids, weekly_bids, last_daily_report, last_weekly_report

    while True:
        now = datetime.now(KYIV_TZ)
        today_str = now.strftime("%Y-%m-%d")
        week_str = now.strftime("%Y-W%W")

        # Дневной отчёт — каждый день в 23:00
        if now.hour == 23 and now.minute == 0 and last_daily_report != today_str:
            last_daily_report = today_str
            report = get_daily_report(daily_bids)
            try:
                bot.send_message(CHAT_ID, report, parse_mode="HTML")
            except Exception as e:
                print(f"❌ Помилка дневного отчёта: {e}")
            daily_bids = 0  # сбрасываем счётчик

        # Недельный отчёт — каждый понедельник в 09:00
        if now.weekday() == 0 and now.hour == 9 and now.minute == 0 and last_weekly_report != week_str:
            last_weekly_report = week_str
            report = get_weekly_report(weekly_bids)
            try:
                bot.send_message(CHAT_ID, report, parse_mode="HTML")
            except Exception as e:
                print(f"❌ Помилка недельного отчёта: {e}")
            weekly_bids = 0  # сбрасываем счётчик

        time.sleep(60)  # проверяем каждую минуту


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
            "link": links.get("web") or f"https://freelancehunt.com/project/{title_to_slug(attrs.get('name',''))}/{project_id}.html"
        }
    except Exception as e:
        print(f"❌ Помилка отримання проекту {project_id}: {e}")
        return {}


# ─── Генерация отклика через Groq ────────────────────────────────────────────

def generate_response(title: str, description: str, lang: str = "UA") -> str:
    system_prompt = SYSTEM_PROMPT_UA if lang == "UA" else SYSTEM_PROMPT_RU
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Назва проекту: {title}\n\nОпис: {description}"}
            ],
            max_tokens=400,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Помилка генерації: {e}"


# ─── Обработчики кнопок ──────────────────────────────────────────────────────

@bot.callback_query_handler(func=lambda call: call.data.startswith("respond_ua_") or call.data.startswith("respond_ru_"))
def handle_respond(call):
    global daily_bids, weekly_bids

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

    # Считаем отклик
    daily_bids += 1
    weekly_bids += 1

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(f"🔄 Ще раз ({lang})", callback_data=f"regen_{lang.lower()}_{project_id}"),
        InlineKeyboardButton("❌ Скасувати", callback_data=f"cancel_{project_id}")
    )

    bot.send_message(
        CHAT_ID,
        f"📋 <b>Скопіюй і встав відгук:</b>\n\n{response_text}\n\n🔗 <a href='{link}'>Відкрити проект</a>\n\n📈 Відгуків сьогодні: <b>{daily_bids}</b> | За тиждень: <b>{weekly_bids}</b>",
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

    link = project["link"]
    bot.edit_message_text(
        f"📋 <b>Новий відгук — скопіюй і встав:</b>\n\n{response_text}\n\n🔗 <a href='{link}'>Відкрити проект</a>\n\n📈 Відгуків сьогодні: <b>{daily_bids}</b> | За тиждень: <b>{weekly_bids}</b>",
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
                    link = links.get("web")
                    # Якщо links.web відсутній або не містить slug — генеруємо самі
                    if not link or link == f"https://freelancehunt.com/project/{project_id}.html":
                        slug = title_to_slug(title)
                        link = f"https://freelancehunt.com/project/{slug}/{project_id}.html"

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


# ─── Запуск ───────────────────────────────────────────────────────────────────

def scheduler():
    print("🚀 Ninja запускається...")
    init_seen_projects()

    try:
        bot.send_message(CHAT_ID, "🚀 Ninja запущений! Gemini AI готовий 🤖\nОбирай мову і копіюй текст 📋\nЩодня о 23:00 — підсумок дня. Понеділок 09:00 — підсумок тижня.")
    except Exception as e:
        print(f"❌ Помилка старту: {e}")

    # Поток для отчётов
    report_thread = threading.Thread(target=reports_scheduler)
    report_thread.daemon = True
    report_thread.start()

    # Поток для polling
    polling_thread = threading.Thread(target=bot.polling, kwargs={"none_stop": True})
    polling_thread.daemon = True
    polling_thread.start()

    # Основной цикл мониторинга проектов
    while True:
        try:
            check_new_projects()
        except Exception as e:
            print(f"❌ Помилка в циклі: {e}")
        time.sleep(300)


if __name__ == "__main__":
    scheduler()
