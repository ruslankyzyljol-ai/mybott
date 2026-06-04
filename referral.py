from telebot import types
from database import get_user, is_vip
from config import VIP_REFERRAL_DAYS

def register_referral(bot):

    @bot.message_handler(func=lambda m: m.text == "👥 Дос чакыр VIP")
    def referral_menu(msg):
        user_id = msg.from_user.id
        user = get_user(user_id)
        refs = len(user.get("referrals", []))
        vip = is_vip(user_id)

        next_goal = None
        for needed in sorted(VIP_REFERRAL_DAYS.keys()):
            if refs < needed:
                next_goal = needed
                break

        link = f"https://t.me/PROFIX_bot?start=REF{user_id}"

        status_text = "👑 VIP активдүү!" if vip else "❌ VIP жок"
        progress = f"Прогресс: {refs}/{next_goal} дос" if next_goal else "Бардык максатка жеттиңиз! 🎉"

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("📤 Шилтеме жиберүү", switch_inline_query=f"PROFIX ботуна кошулуңуз! {link}"))

        rewards_text = "\n".join([
            f"👤 {n} дос = {d} күн VIP"
            for n, d in sorted(VIP_REFERRAL_DAYS.items())
        ])

        bot.send_message(msg.chat.id,
            f"👥 *Дос чакыр — VIP ал*\n\n"
            f"💎 Статус: {status_text}\n"
            f"👥 Чакырдыңыз: {refs} дос\n"
            f"📈 {progress}\n\n"
            f"🎁 *Сыйлыктар:*\n{rewards_text}\n\n"
            f"🔗 *Сенин шилтемең:*\n`{link}`\n\n"
            f"📋 Шилтемени көчүрүп досторуңузга жибериңиз!",
            parse_mode="Markdown", reply_markup=kb)
