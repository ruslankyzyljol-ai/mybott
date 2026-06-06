import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
FOOTBALL_API = os.environ.get("FOOTBALL_API", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@profix_news")

BOOKMAKERS = {
    "1win": {
        "name": "1Win",
        "emoji": "🏆",
        "link": os.environ.get("LINK_1WIN", "https://1win.kg"),
        "promo": os.environ.get("PROMO_1WIN", "WIN500"),
        "bonus": "+200% биринчи депозитке"
    },
    "1xbet": {
        "name": "1xBet",
        "emoji": "⚡",
        "link": os.environ.get("LINK_1XBET", "https://1xbet.kg"),
        "promo": os.environ.get("PROMO_1XBET", "BET300"),
        "bonus": "+130% биринчи депозитке"
    },
    "melbet": {
        "name": "Melbet",
        "emoji": "🎯",
        "link": os.environ.get("LINK_MELBET", "https://melbet.kg"),
        "promo": os.environ.get("PROMO_MELBET", "MEL200"),
        "bonus": "+100% биринчи депозитке"
    }
}

VIP_REFERRAL_DAYS = {1: 3, 3: 14, 5: 30}
