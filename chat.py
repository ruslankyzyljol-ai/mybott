from telebot import types
import random

SPORT_ANSWERS = [
    "Бул команда акыркы матчтарда жакшы форм көрсөтүп жатат. Статистика боюнча жеңүү мүмкүнчүлүгү жогору.",
    "Травмалар жана дисквалификациялар командага таасир этип жатат. Башкы оюнчулар жок болушу натыйжага таасир берет.",
    "Эки команда тең күчтүү. Бирок үй ээсинин артыкчылыгы бар — статистика ошону көрсөтөт.",
    "Акыркы беттешүүлөрдө бул команда утуп алган. Психологиялык артыкчылык бар.",
    "Коноктор жол оюндарында алсызыраак. Үй команданын 60% мүмкүнчүлүгү бар.",
    "Орто мелдеш болуп жатат. Эки жак тең чабуул тактикасын колдонот.",
    "Акыркы 5 матчта бул команда 4 жолу утуп алды. Жакшы форм!",
]

def get_ai_response(question):
    q = question.lower()
    if any(w in q for w in ["неге", "эмне үчүн", "себеп"]):
        return random.choice([
            "Бул бир нече себептерге байланыштуу: травмалар, форм жана тактика.",
            "Статистика боюнча бул команда мындай шарттарда начарлайт.",
            "Тренердин тактикасы жана оюнчулардын физикалык абалы чечүүчү фактор."
        ])
    if any(w in q for w in ["утат", "жеңет", "кайсы"]):
        return random.choice(SPORT_ANSWERS)
    if any(w in q for w in ["ойнобойт", "жок", "травма"]):
        return "Травмалар жана дисквалификациялар — маанилүү фактор. Башкы оюнчу жок болсо команда 20-30% алсызданат."
    if any(w in q for w in ["коэф", "ставка", "кой"]):
        return "Ставка коюуда: жогорку коэф = жогорку тобокел. Акча башкаруу маанилүү — бир ставкага 5-10% гана."
    return random.choice(SPORT_ANSWERS)

def register_chat(bot):

    user_chat_mode = {}

    @bot.message_handler(func=lambda m: m.text == "💬 AI Чат")
    def ai_chat(msg):
        user_chat_mode[msg.from_user.id] = True
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("🔙 Башкы менюга")
        bot.send_message(msg.chat.id,
            "💬 *AI Чат*\n\n"
            "Саламатсызбы! Спорт жана оюндар жөнүндө каалаган суроону бериңиз.\n\n"
            "Мисалы:\n"
            "• Холанд эмне үчүн ойнобойт?\n"
            "• Кайсы команда утат?\n"
            "• Авиатор стратегиясы кандай?",
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
        response = get_ai_response(msg.text)
        bot.send_message(msg.chat.id,
            f"🤖 *PROFIX AI:*\n\n{response}\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🎁 Ставка коюгуңуз келсе:\n"
            f"Негизги менюдан *🎁 Бонустар* басыңыз",
            parse_mode="Markdown")
