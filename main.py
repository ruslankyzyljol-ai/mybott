import telebot
import threading
import schedule
import time
from config import BOT_TOKEN
import start
import sports
import games
import bonus
import admin
import referral
import chat
import match_updater

bot = telebot.TeleBot(BOT_TOKEN)

start.register_start(bot)
sports.register_sports(bot)
games.register_games(bot)
bonus.register_bonus(bot)
admin.register_admin(bot)
referral.register_referral(bot)
chat.register_chat(bot)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

match_updater.start_match_updater(bot)
t = threading.Thread(target=run_scheduler)
t.daemon = True
t.start()
bot.infinity_polling()
