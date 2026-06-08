from telebot import types
import requests
import os
import random

GEMINI_API = os.environ.get("GEMINI_API", "")

ANSWERS = [
    "Бул команда акыркы матчтарда жакшы форм көрсөтүп жатат. Жеңүү мүмкүнчүлүгү жогору.",
    "Травмалар таасир этип жатат. Башкы оюнчулар жок болушу натыйжага таасир берет.",
    "Эки команда тең күчтүү. Үй ээсинин артыкчылыгы бар.",
    "Акыркы 5 матчта бул команда 4 жолу утуп алды. Жакшы форм!",
]

def get_ai_response(question):
    if GEMINI_API:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API}"
            body = {
                "contents": [{
                    "parts": [{
                        "text": f"Сен PROFIX деген спорт анализ ботусуң. Кыргызча жооп бер. Суроо: {question}"
                    }]
                }]
            }
            r = requests.post(url, json=body, timeout=10)
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            pass
    return random.choice(ANSWERS)

def register_chat(bot):
    user_chat_mode = {}

    @bot.message_handler(func=lambda m: m.text == "💬 AI Чат")
    def ai_chat(msg):
        user_chat_mode[msg.from_user.id] = True
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("🔙 Башкы менюга")
        bot.send_message(msg.chat.id,
            "💬 *AI Чат*\n\nСаламатсызбы! Спорт жана оюндар жөнүндө каалаган суроону бериңиз.\n\n"
            "Мисалы:\n• Холанд эмне үчүн ойнобойт?\n• Кайсы команда утат?\n• Авиатор стратегиясы?",
            parse_mode="Markdown", reply_markup=kb)

    @bot.message_handler(func=lambda m: m.text == "🔙 Башкы менюга")
    def back_main(msg):
        user_chat_mode.pop(msg.from_user.id, None)
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("⚽ Спорт анализ", "🎮 Оюн сигналы")
        kb.row("🎁 Бонустар", "👥 Дос чакыр VIP")
        kb.row("💬 AI Чат", "👤 Профилим")
        bot.send_message(msg.chat.id, "🏠 Башкы меню", reply_markup=kb)

    @bot.message_handler(func=lambda m: user_chat_mode.get(m.from_user.id))
    def handle_chat(msg):
        bot.send_chat_action(msg.chat.id, "typing")
        bot.send_message(msg.chat.id,
            f"🤖 *PROFIX AI:*\n\n{get_ai_response(msg.text)}\n\n"
            f"━━━━━━━━━━━━━━━\n🎁 Ставка үчүн: *🎁 Бонустар* бөлүмүн ачыңыз",
            parse_mode="Markdown")
