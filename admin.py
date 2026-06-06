from telebot import types
from config import ADMIN_ID
from database import get_all_users, set_link, set_vip, get_matches
import time

def register_admin(bot):
    def is_admin(uid):
        return uid == ADMIN_ID

    @bot.message_handler(commands=["admin"])
    def admin_panel(msg):
        if not is_admin(msg.from_user.id): return
        users = get_all_users()
        matches = get_matches()
        active = len([m for m in matches if not m.get("finished")])
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("📊 Статистика", callback_data="adm_stats"))
        kb.add(types.InlineKeyboardButton("📢 Жарыя жибер", callback_data="adm_broadcast"))
        bot.send_message(msg.chat.id,
            f"🔐 *Админ панель*\n\n👥 Колдонуучулар: {len(users)}\n⚽ Активдүү матчтар: {active}",
            parse_mode="Markdown", reply_markup=kb)

    @bot.callback_query_handler(func=lambda c: c.data == "adm_stats")
    def admin_stats(call):
        if not is_admin(call.from_user.id): return
        users = get_all_users()
        vip_count = sum(1 for u in users.values() if u.get("vip"))
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
            f"📊 *Статистика*\n\n👥 Жалпы: {len(users)}\n👑 VIP: {vip_count}\n👤 Кадимки: {len(users)-vip_count}",
            parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda c: c.data == "adm_broadcast")
    def admin_broadcast(call):
        if not is_admin(call.from_user.id): return
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "📢 Жарыя текстин жазыңыз (фото да жиберсе болот):")
        bot.register_next_step_handler(msg, do_broadcast)

    def do_broadcast(msg):
        if not is_admin(msg.from_user.id): return
        users = get_all_users()
        sent = 0
        for uid in list(users.keys()):
            try:
                if msg.photo:
                    bot.send_photo(int(uid), msg.photo[-1].file_id, caption=msg.caption or "")
                else:
                    bot.send_message(int(uid), msg.text)
                sent += 1
                time.sleep(0.05)
            except:
                pass
        bot.send_message(msg.chat.id, f"✅ Жиберилди! {sent}/{len(users)}")

    @bot.message_handler(commands=["setlink"])
    def set_link_cmd(msg):
        if not is_admin(msg.from_user.id): return
        parts = msg.text.split()
        if len(parts) < 4:
            bot.send_message(msg.chat.id, "Формат: /setlink 1win https://ссылка.com PROMO123")
            return
        set_link(parts[1].lower(), parts[2], parts[3])
        bot.send_message(msg.chat.id, f"✅ {parts[1].upper()} жаңыланды!\n🔗 {parts[2]}\n🎁 {parts[3]}")

    @bot.message_handler(commands=["setvip"])
    def set_vip_cmd(msg):
        if not is_admin(msg.from_user.id): return
        parts = msg.text.split()
        if len(parts) < 3:
            bot.send_message(msg.chat.id, "Формат: /setvip 123456789 30")
            return
        set_vip(int(parts[1]), int(parts[2]))
        bot.send_message(msg.chat.id, f"✅ {parts[1]} га {parts[2]} күн VIP берилди!")

    @bot.message_handler(commands=["stats"])
    def stats(msg):
        if not is_admin(msg.from_user.id): return
        users = get_all_users()
        vip_count = sum(1 for u in users.values() if u.get("vip"))
        bot.send_message(msg.chat.id,
            f"📊 *Статистика*\n\n👥 Жалпы: {len(users)}\n👑 VIP: {vip_count}",
            parse_mode="Markdown")
