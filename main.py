import telebot
import threading
import schedule
import time
from telebot import types
from config import BOT_TOKEN, ADMIN_ID
from handlers.start import register_start
from handlers.sports import register_sports
from handlers.games import register_games
from handlers.bonus import register_bonus
from handlers.admin import register_admin
from handlers.referral import register_referral
from handlers.chat import register_chat
from utils.match_updater import start_match_updater

bot = telebot.TeleBot(BOT_TOKEN)

register_start(bot)
register_sports(bot)
register_games(bot)
register_bonus(bot)
register_admin(bot)
register_referral(bot)
register_chat(bot)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    print("PROFIX бот иштеп баштады...")
    start_match_updater(bot)
    t = threading.Thread(target=run_scheduler)
    t.daemon = True
    t.start()
    bot.infinity_polling()
