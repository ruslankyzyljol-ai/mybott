from telebot import types
from database import get_user, save_user, add_referral
from config import CHANNEL_ID

def register_start(bot):

    def check_subscribed(user_id):
        try:
            member = bot.get_chat_member(CHANNEL_ID, user_id)
            return member.status in ["member", "administrator", "creator"]
        except:
            return True

    def main_menu(user_id):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("⚽ Спорт анализ", "🎮 Оюн сигналы")
        kb.row("🎁 Бонустар", "👥 Дос чакыр VIP")
        kb.row("💬 AI Чат", "👤 Профилим")
        return kb

    @bot.message_handler(commands=["start"])
    def start(msg):
        user_id = msg.from_user.id
        args = msg.text.split()
        user = get_user(user_id)

        if len(args) > 1 and args[1].startswith("REF"):
            ref_id = args[1].replace("REF", "")
            if ref_id != str(user_id) and not user.get("referred_by"):
                user["referred_by"] = ref_id
                save_user(user_id, user)
                days = add_referral(ref_id, user_id)
                if days > 0:
                    try:
                        bot.send_message(int(ref_id),
                            f"🎉 Жаңы дос кирди! Сиз {days} күн VIP алдыңыз! 👑")
                    except:
                        pass

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(
            "📢 Каналга жазыл", url=f"https://t.me/{CHANNEL_ID.replace('@','')}"))
        kb.add(types.InlineKeyboardButton("✅ Жазылдым — текшер", callback_data="check_sub"))

        bot.send_message(user_id,
            "⚡ *PROFIX* ботуна кош келдиңиз\\!\n\n"
            "✅ AI матч анализ — кыргызча\n"
            "✅ Авиатор · Чикен сигналдары\n"
            "✅ Промокод \\+ бонустар\n"
            "✅ 24/7 суроо\\-жооп чат\n\n"
            "👇 Уланууга каналга жазылыңыз:",
            parse_mode="MarkdownV2", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "check_sub")
    def check_sub(call):
        user_id = call.from_user.id
        if check_subscribed(user_id):
            bot.answer_callback_query(call.id, "✅ Текшерилди!")
            bot.send_message(user_id,
                "🎉 Кош келдиңиз\\! Меню төмөндө 👇",
                parse_mode="MarkdownV2",
                reply_markup=main_menu(user_id))
        else:
            bot.answer_callback_query(call.id, "❌ Каналга жазылыңыз!", show_alert=True)

    @bot.message_handler(func=lambda m: m.text == "👤 Профилим")
    def profile(msg):
        from database import is_vip, get_user
        user_id = msg.from_user.id
        user = get_user(user_id)
        vip = is_vip(user_id)
        refs = len(user.get("referrals", []))
        vip_text = f"👑 VIP: ✅ {user.get('vip_until','')[:10]}" if vip else "👑 VIP: ❌"
        bot.send_message(user_id,
            f"👤 *Профилиңиз*\n\n"
            f"🆔 ID: `{user_id}`\n"
            f"{vip_text}\n"
            f"👥 Чакырылган досторуңуз: {refs}\n\n"
            f"Дос чакыруу шилтемеңиз:\n"
            f"`t.me/PROFIX_bot?start=REF{user_id}`",
            parse_mode="Markdown")
