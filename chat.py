from telebot import types
import random

ANSWERS = [
    "Бул команда акыркы матчтарда жакшы форм көрсөтүп жатат. Жеңүү мүмкүнчүлүгү жогору.",
    "Травмалар жана дисквалификациялар таасир этип жатат. Башкы оюнчулар жок болушу натыйжага таасир берет.",
    "Эки команда тең күчтүү. Үй ээсинин артыкчылыгы бар — статистика ошону көрсөтөт.",
    "Акыркы беттешүүлөрдө бул команда жакшы натыйжа көрсөттү.",
    "Акыркы 5 матчта бул команда 4 жолу утуп алды. Жакшы форм!",
    "Статистика боюнча үй командасы 60% мүмкүнчүлүккө ээ.",
]

def get_ai_response(question):
    q = question.lower() if question else ""
    if any(w in q for w in ["неге", "эмне", "себеп"]):
        return "Бул бир нече себептерге байланыштуу: травмалар, форм жана тактика айырмасы чечүүчү роль ойнойт."
    if any(w in q for w in ["травма", "ойнобойт", "жок"]):
        return "Башкы оюнчу жок болсо команда 20-30% алсызданат. Ордун баскан оюнчунун деңгээлине жараша болот."
    if any(w in q for w in ["ставка", "коэф", "кой"]):
        return "Ставка коюуда: бир ставкага 5-10% гана бөлүңүз. Жогорку коэф = жогорку тобокел."
    return random.choice(ANSWERS)

def register_chat(bot):
    user_chat_mode = {}

    @bot.message_handler(func=lambda m: m.text == "💬 AI Чат")
    def ai_chat(msg):
        user_chat_mode[msg.from_user.id] = True
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("🔙 Башкы менюга")
        bot.send_message(msg.chat.id,
            "💬 *AI Чат*\n\nСаламатсызбы! Спорт жана оюндар жөнүндө каалаган суроону бериңиз.\n\n"
            "Мисалы:\n• Холанд эмне үчүн ойнобойт?\n• Кайсы команда утат?\n• Авиатор стратегиясы?",
            parse_mode="Markdown", reply_markup=kb)

    @bot.message_handler(func=lambda m: m.text == "🔙 Башкы менюга")
    def back_main(msg):
        user_chat_mode.pop(msg.from_user.id, None)
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("⚽ Спорт анализ", "🎮 Оюн сигналы")
        kb.row("🎁 Бонустар", "👥 Дос чакыр VIP")
        kb.row("💬 AI Чат", "👤 Профилим")
        bot.send_message(msg.chat.id, "🏠 Башкы меню", reply_markup=kb)

    @bot.message_handler(func=lambda m: user_chat_mode.get(m.from_user.id))
    def handle_chat(msg):
        bot.send_chat_action(msg.chat.id, "typing")
        bot.send_message(msg.chat.id,
            f"🤖 *PROFIX AI:*\n\n{get_ai_response(msg.text)}\n\n"
            f"━━━━━━━━━━━━━━━\n🎁 Ставка үчүн: *🎁 Бонустар* бөлүмүн ачыңыз",
            parse_mode="Markdown")
