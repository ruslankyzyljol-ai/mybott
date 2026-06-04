from telebot import types
from database import get_matches, is_vip
import requests
import random

def analyze_match(home, away, league):
    home_win = random.randint(35, 55)
    away_win = random.randint(20, 45)
    draw = 100 - home_win - away_win
    if draw < 10:
        draw = 10
        away_win = 100 - home_win - draw

    forms = ["Ж", "Е", "Т"]
    home_form = " · ".join([random.choice(forms) for _ in range(5)])
    away_form = " · ".join([random.choice(forms) for _ in range(5)])

    goals = ["1-0", "2-1", "1-1", "2-0", "3-1", "0-0", "2-2"]
    prediction = random.choice(goals)

    tips = [
        f"{home} үй ээси катары күчтүүрөөк",
        f"{away} акыркы матчтарда жакшы форм көрсөттү",
        f"Эки команда тең чабуулчан ойнойт",
        f"Дарвазачылар күчтүү — аз гол болушу мүмкүн",
        f"{home} акыркы 3 матчта утуп алды"
    ]

    text = (
        f"📊 *{home} vs {away}*\n"
        f"🏆 {league}\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📈 *Жеңүү мүмкүнчүлүгү:*\n"
        f"🔵 {home}: *{home_win}%*\n"
        f"⚪ Тең: *{draw}%*\n"
        f"🔴 {away}: *{away_win}%*\n\n"
        f"📋 *Акыркы 5 матч:*\n"
        f"{home}: {home_form}\n"
        f"{away}: {away_form}\n\n"
        f"⚡ *Болжол:* {home} {prediction} {away}\n"
        f"💡 *Кеңеш:* {random.choice(tips)}\n"
        f"━━━━━━━━━━━━━━━"
    )
    return text

def register_sports(bot):

    @bot.message_handler(func=lambda m: m.text == "⚽ Спорт анализ")
    def sports_menu(msg):
        matches = get_matches()
        if not matches:
            bot.send_message(msg.chat.id,
                "⏳ Матчтар жүктөлүүдө... Бир аздан кийин кайра басыңыз.")
            return

        kb = types.InlineKeyboardMarkup()
        shown = 0
        for m in matches[:10]:
            if not m.get("finished"):
                label = f"⚽ {m['home'][:12]} vs {m['away'][:12]} · {m['time'][11:16]}"
                kb.add(types.InlineKeyboardButton(
                    label, callback_data=f"match_{m['id']}"))
                shown += 1
            if shown >= 8:
                break

        if shown == 0:
            bot.send_message(msg.chat.id,
                "📅 Азыр жакын арада матч жок. Кийинчерээк кайра кириңиз.")
            return

        bot.send_message(msg.chat.id,
            "📅 *Жакын арадагы матчтар:*\n\nТандаңыз 👇",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("match_"))
    def match_detail(call):
        match_id = int(call.data.replace("match_", ""))
        matches = get_matches()
        match = next((m for m in matches if m["id"] == match_id), None)

        if not match:
            bot.answer_callback_query(call.id, "Матч табылган жок")
            return

        bot.answer_callback_query(call.id, "⏳ Анализ жасалууда...")
        bot.send_chat_action(call.message.chat.id, "typing")

        analysis = analyze_match(match["home"], match["away"], match["league"])

        from database import get_link
        from config import BOOKMAKERS
        bm = get_link("1win") or BOOKMAKERS["1win"]
        link = bm.get("link", BOOKMAKERS["1win"]["link"])
        promo = bm.get("promo", BOOKMAKERS["1win"]["promo"])

        promo_text = (
            f"\n🎁 *Ставка коюп бонус ал:*\n"
            f"🔗 [1Win ге кир]({link})\n"
            f"📝 Промокод: `{promo}`\n"
            f"💰 Биринчи депозитке +200% бонус\\!"
        )

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🚀 1Win ге кир", url=link))
        kb.add(types.InlineKeyboardButton("💬 Суроо бер", callback_data=f"ask_match_{match_id}"))

        bot.send_message(call.message.chat.id,
            analysis + promo_text,
            parse_mode="Markdown", reply_markup=kb,
            disable_web_page_preview=True)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("ask_match_"))
    def ask_about_match(call):
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
            "💬 Бул матч жөнүндө кандай сурооңуз бар?\n\nЖазыңыз 👇")
        bot.register_next_step_handler(call.message, handle_match_question)

    def handle_match_question(msg):
        from handlers.chat import get_ai_response
        bot.send_chat_action(msg.chat.id, "typing")
        response = get_ai_response(msg.text)
        bot.send_message(msg.chat.id, response)
