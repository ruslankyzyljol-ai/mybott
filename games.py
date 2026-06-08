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
        bot.send_message(msg.chat.id, "🎮 *Оюн тандаңыз:*", parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "game_aviator")
    def aviator(call):
        bot.answer_callback_query(call.id, "⏳ Сигнал...")
        coef = round(random.uniform(1.3, 8.5), 2)
        history = [round(random.uniform(1.1, 7.0), 2) for _ in range(5)]
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔄 Жаңы сигнал", callback_data="game_aviator"))
        bot.send_message(call.message.chat.id,
            f"✈️ *АВИАТОР СИГНАЛЫ*\n\n🎯: *{coef}x*\n⏱ 2 мүнөт жарактуу\n\n"
            f"📊 Акыркы 5: {' · '.join([str(h)+'x' for h in history])}\n\n"
            f"⚠️ 100%",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "game_chicken")
    def chicken(call):
        bot.answer_callback_query(call.id, "⏳ Сигнал...")
        multiplier = round(random.uniform(1.5, 15.0), 2)
        bombs = random.randint(1, 5)
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔄 Жаңы сигнал", callback_data="game_chicken"))
        bot.send_message(call.message.chat.id,
            f"🐔 *ЧИКЕН СИГНАЛЫ*\n\n🎯 Коэф: *{multiplier}x*\n💣 Бомба: {bombs}\n"
            f"💡 {multiplier}x га жеткенде чыгыңыз\n\n 100%",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "game_crash")
    def crash(call):
        bot.answer_callback_query(call.id, "⏳ Сигнал...")
        coef = round(random.uniform(1.2, 6.0), 2)
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔄 Жаңы сигнал", callback_data="game_crash"))
        bot.send_message(call.message.chat.id,
            f"💥 *КРАШ СИГНАЛЫ*\n\n🎯 Чыгуу: *{coef}x*\n\n 100%",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "game_slot")
    def slot(call):
        bot.answer_callback_query(call.id)
        symbols = ["🍒","🍋","🍊","🍇","⭐","💎","7️⃣"]
        result = [random.choice(symbols) for _ in range(3)]
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔄 Дагы", callback_data="game_slot"))
        if result[0] == result[1] == result[2]:
            txt = "🎉 ДЖЕКПОТ!"
        elif result[0]==result[1] or result[1]==result[2]:
            txt = "✅ Жакшы!"
        else:
            txt = "🔄 Дагы айлантыңыз!"
        bot.send_message(call.message.chat.id,
            f"🎰 {' '.join(result)}\n\n{txt}", reply_markup=kb)
