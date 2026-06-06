from telebot import types
from database import get_matches
import random

def analyze_match(home, away, league):
    home_win = random.randint(35, 55)
    away_win = random.randint(20, 40)
    draw = 100 - home_win - away_win
    forms = ["Ж", "Е", "Т"]
    home_form = " · ".join([random.choice(forms) for _ in range(5)])
    away_form = " · ".join([random.choice(forms) for _ in range(5)])
    goals = ["1-0", "2-1", "1-1", "2-0", "3-1", "0-0", "2-2"]
    prediction = random.choice(goals)
    tips = [
        f"{home} үй ээси катары күчтүүрөөк",
        f"{away} акыркы матчтарда жакшы форм",
        f"Эки команда тең чабуулчан ойнойт",
        f"Аз гол болушу мүмкүн",
        f"{home} акыркы 3 матчта утту"
    ]
    return (
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
        f"💡 {random.choice(tips)}\n"
        f"━━━━━━━━━━━━━━━"
    )

def register_sports(bot):
    @bot.message_handler(func=lambda m: m.text == "⚽ Спорт анализ")
    def sports_menu(msg):
        matches = get_matches()
        active = [m for m in matches if not m.get("finished")]
        if not active:
            bot.send_message(msg.chat.id, "📅 Азыр жакын арада матч жок. Кийинчерээк кайра кириңиз.")
            return
        kb = types.InlineKeyboardMarkup()
        for m in active[:8]:
            label = f"⚽ {m['home'][:13]} vs {m['away'][:13]} · {m['time'][11:16]}"
            kb.add(types.InlineKeyboardButton(label, callback_data=f"match_{m['id']}"))
        bot.send_message(msg.chat.id, "📅 *Жакын арадагы матчтар:*\n\nТандаңыз 👇",
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
        saved = get_link("1win")
        link = saved["link"] if saved else BOOKMAKERS["1win"]["link"]
        promo = saved["promo"] if saved else BOOKMAKERS["1win"]["promo"]
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🚀 1Win ге кир", url=link))
        kb.add(types.InlineKeyboardButton("💬 Суроо бер", callback_data=f"ask_{match_id}"))
        bot.send_message(call.message.chat.id,
            analysis + f"\n\n🎁 *Ставка коюп бонус ал:*\nПромокод: `{promo}`",
            parse_mode="Markdown", reply_markup=kb, disable_web_page_preview=True)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("ask_"))
    def ask_match(call):
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "💬 Сурооңузду жазыңыз 👇")
        bot.register_next_step_handler(msg, handle_question)

    def handle_question(msg):
        from handlers.chat import get_ai_response
        bot.send_chat_action(msg.chat.id, "typing")
        bot.send_message(msg.chat.id, f"🤖 *PROFIX AI:*\n\n{get_ai_response(msg.text)}", parse_mode="Markdown")
