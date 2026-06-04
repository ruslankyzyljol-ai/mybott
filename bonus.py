from telebot import types
from config import BOOKMAKERS
from database import get_link

def register_bonus(bot):

    @bot.message_handler(func=lambda m: m.text == "🎁 Бонустар")
    def bonus_menu(msg):
        kb = types.InlineKeyboardMarkup()
        for key, bm in BOOKMAKERS.items():
            kb.add(types.InlineKeyboardButton(
                f"{bm['emoji']} {bm['name']} — {bm['bonus']}",
                callback_data=f"bonus_{key}"))
        bot.send_message(msg.chat.id,
            "🎁 *Бонустар менен платформалар:*\n\nТандаңыз 👇",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data.startswith("bonus_"))
    def show_bonus(call):
        key = call.data.replace("bonus_", "")
        bm = BOOKMAKERS.get(key, {})
        saved = get_link(key)

        link = saved["link"] if saved else bm.get("link", "#")
        promo = saved["promo"] if saved else bm.get("promo", "")

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(
            f"🚀 {bm['name']} ге кир", url=link))
        kb.add(types.InlineKeyboardButton(
            "⬅️ Артка", callback_data="back_bonus"))

        bot.edit_message_text(
            f"{bm['emoji']} *{bm['name']} — Бонус алуу*\n\n"
            f"📝 *Кадамдар:*\n\n"
            f"1️⃣ Төмөндөгү ссылкадан кириңиз\n"
            f"2️⃣ Жаңы акк ачыңыз\n"
            f"3️⃣ Каттоодо промокод жазыңыз:\n\n"
            f"🎁 Промокод: `{promo}`\n\n"
            f"4️⃣ Биринчи депозит коюңуз\n"
            f"✅ *{bm['bonus']}* автоматтык активдешет\\!",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="MarkdownV2",
            reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "back_bonus")
    def back_bonus(call):
        kb = types.InlineKeyboardMarkup()
        for key, bm in BOOKMAKERS.items():
            kb.add(types.InlineKeyboardButton(
                f"{bm['emoji']} {bm['name']} — {bm['bonus']}",
                callback_data=f"bonus_{key}"))
        bot.edit_message_text(
            "🎁 *Бонустар менен платформалар:*\n\nТандаңыз 👇",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown", reply_markup=kb)
