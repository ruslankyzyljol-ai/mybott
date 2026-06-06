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
        next_goal = next((n for n in sorted(VIP_REFERRAL_DAYS.keys()) if refs < n), None)
        link = f"https://t.me/PROFIX_bot?start=REF{user_id}"
        status = "👑 VIP активдүү!" if vip else "❌ VIP жок"
        progress = f"{refs}/{next_goal} дос" if next_goal else "Баары бүттү! 🎉"
        rewards = "\n".join([f"👤 {n} дос = {d} күн VIP" for n, d in sorted(VIP_REFERRAL_DAYS.items())])
        bot.send_message(msg.chat.id,
            f"👥 *Дос чакыр — VIP ал*\n\n"
            f"💎 {status}\n👥 Чакырдыңыз: {refs} дос\n📈 {progress}\n\n"
            f"🎁 *Сыйлыктар:*\n{rewards}\n\n"
            f"🔗 *Шилтемең:*\n`{link}`",
            parse_mode="Markdown")
