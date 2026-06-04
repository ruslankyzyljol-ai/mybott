from telebot import types
import random

def register_games(bot):

    @bot.message_handler(func=lambda m: m.text == "🎮 Оюн сигналы")
    def games_menu(msg):
        kb = types.InlineKeyboardMarkup()
        kb.row(
            types.InlineKeyboardButton("✈️ Авиатор", callback_data="game_aviator"),
            types.InlineKeyboardButton("🐔 Чикен", callback_data="game_chicken")
        )
        kb.row(
            types.InlineKeyboardButton("💥 Краш", callback_data="game_crash"),
            types.InlineKeyboardButton("🎰 Слот", callback_data="game_slot")
        )
        bot.send_message(msg.chat.id,
            "🎮 *Оюн тандаңыз:*",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "game_aviator")
    def aviator(call):
        bot.answer_callback_query(call.id, "⏳ Сигнал эсептелүүдө...")
        coef = round(random.uniform(1.3, 8.5), 2)
        history = [round(random.uniform(1.1, 7.0), 2) for _ in range(5)]

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔄 Жаңы сигнал", callback_data="game_aviator"))
        kb.add(types.InlineKeyboardButton("🚀 1Win де ойно", url="https://1win.kg"))

        bot.send_message(call.message.chat.id,
            f"✈️ *АВИАТОР СИГНАЛЫ*\n\n"
            f"🎯 Кийинки болжол: *{coef}x*\n"
            f"⏱ Жарактуулук: 2 мүнөт\n\n"
            f"📊 Акыркы 5 учуу:\n"
            f"{' · '.join([str(h)+'x' for h in history])}\n\n"
            f"⚠️ Бул болжол — 100% кепилдик эмес",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "game_chicken")
    def chicken(call):
        bot.answer_callback_query(call.id, "⏳ Сигнал эсептелүүдө...")
        multiplier = round(random.uniform(1.5, 15.0), 2)
        bombs = random.randint(1, 5)
        safe = 25 - bombs

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔄 Жаңы сигнал", callback_data="game_chicken"))

        bot.send_message(call.message.chat.id,
            f"🐔 *ЧИКЕН СИГНАЛЫ*\n\n"
            f"🎯 Сунушталган коэф: *{multiplier}x*\n"
            f"💣 Бомба саны: {bombs}\n"
            f"✅ Коопсуз уяча: {safe}\n\n"
            f"💡 *Стратегия:* {multiplier}x га жеткенде чыгыңыз\n\n"
            f"⚠️ Бул болжол — 100% кепилдик эмес",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "game_crash")
    def crash(call):
        bot.answer_callback_query(call.id, "⏳ Сигнал эсептелүүдө...")
        coef = round(random.uniform(1.2, 6.0), 2)

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔄 Жаңы сигнал", callback_data="game_crash"))

        bot.send_message(call.message.chat.id,
            f"💥 *КРАШ СИГНАЛЫ*\n\n"
            f"🎯 Чыгуу чекити: *{coef}x*\n\n"
            f"💡 *Кеңеш:* {coef}x га жеткенде дароо чыгыңыз\n\n"
            f"⚠️ Бул болжол — 100% кепилдик эмес",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "game_slot")
    def slot(call):
        bot.answer_callback_query(call.id)
        symbols = ["🍒", "🍋", "🍊", "🍇", "⭐", "💎", "7️⃣"]
        result = [random.choice(symbols) for _ in range(3)]

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔄 Дагы айлантуу", callback_data="game_slot"))

        if result[0] == result[1] == result[2]:
            msg_text = f"🎰 {' '.join(result)}\n\n🎉 ДЖЕКПОТ! Ойноп көрүңүз!"
        elif result[0] == result[1] or result[1] == result[2]:
            msg_text = f"🎰 {' '.join(result)}\n\n✅ Жакшы комбинация!"
        else:
            msg_text = f"🎰 {' '.join(result)}\n\n🔄 Дагы айлантыңыз!"

        bot.send_message(call.message.chat.id,
            f"🎰 *СЛОТ ДЕМО*\n\n{msg_text}",
            parse_mode="Markdown", reply_markup=kb)
