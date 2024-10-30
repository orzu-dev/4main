from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Loggingni o'rnatish
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot tokenini kiriting
BOT_TOKEN = '7649991283:AAFJyCVNzD4kNkuv-PxGy4euG8_Vx5bbAq0'

# Majburiy kanallar
CHANNELS = {
    'Kanal 1': 'https://t.me/onlinesearchbook',
    'Kanal 2': 'https://t.me/tabriknoma_uzbekistann'
}

# Nomzodlar va ularning ovozlari
candidates = {
    'Nomzod 1': {'video': 'https://www.example.com/video1.mp4', 'votes': 0},
    'Nomzod 2': {'video': 'https://www.example.com/video2.mp4', 'votes': 0},
    'Nomzod 3': {'video': 'https://www.example.com/video3.mp4', 'votes': 0},
    'Nomzod 4': {'video': 'https://www.example.com/video4.mp4', 'votes': 0},
    'Nomzod 5': {'video': 'https://www.example.com/video5.mp4', 'votes': 0},
    'Nomzod 6': {'video': 'https://www.example.com/video6.mp4', 'votes': 0},
    'Nomzod 7': {'video': 'https://www.example.com/video7.mp4', 'votes': 0},
    'Nomzod 8': {'video': 'https://www.example.com/video8.mp4', 'votes': 0},
    'Nomzod 9': {'video': 'https://www.example.com/video9.mp4', 'votes': 0},
    'Nomzod 10': {'video': 'https://www.example.com/video10.mp4', 'votes': 0}
}

# Foydalanuvchilarning ovoz bergan IP adreslari
user_votes = {}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton(name, url=url) for name, url in CHANNELS.items()],
        [InlineKeyboardButton("Obuna bo'ldim", callback_data="check_subscription")]
    ]
    await update.message.reply_text(
        f"Salom, {user.first_name}! Quyidagi kanallarga obuna bo'ling va \"Obuna bo'ldim\" tugmasini bosing:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Obuna holatini tekshirish
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    all_subscribed = True

    for channel_name, channel_url in CHANNELS.items():
        chat_member = await context.bot.get_chat_member(channel_url.split('/')[-1], user_id)
        if chat_member.status not in ['member', 'administrator', 'creator']:
            all_subscribed = False
            await query.answer(f"Siz {channel_name} kanaliga obuna emassiz!")
            return

    if all_subscribed:
        await query.message.reply_text("Siz barcha kanallarga obuna bo'lgansiz! Ovoz berish menyusiga o'ting.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ovoz berish", callback_data="vote_menu")]]))

# Ovoz berish menyusi
async def vote_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    buttons = [[InlineKeyboardButton(f"{name} - {info['votes']} ovoz", callback_data=name)] for name, info in candidates.items()]
    await query.message.reply_text("Iltimos, ovoz berishni istagan nomzodni tanlang:", reply_markup=InlineKeyboardMarkup(buttons))

# Nomzod menyusi
async def candidate_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    candidate_name = query.data
    candidate_info = candidates[candidate_name]
    
    buttons = [
        [InlineKeyboardButton("Ovoz berish", callback_data=f'vote_{candidate_name}'), InlineKeyboardButton("Ulashish", url=candidate_info['video'])],
        [InlineKeyboardButton("Orqaga", callback_data='vote_menu')]
    ]

    await query.message.reply_text(
        f"{candidate_name}:\nVideo: {candidate_info['video']}\nOvozlar: {candidate_info['votes']}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Ovoz berish funksiyasi
async def cast_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    candidate_name = query.data.split('_')[1]
    
    # Foydalanuvchining IP adresini olish
    user_ip = update.effective_user.id  # Bu yerda haqiqiy IP adres olish uchun usulni sozlashingiz mumkin

    # Faqat bitta ovoz berishni ta'minlash
    if user_ip in user_votes and user_votes[user_ip] == candidate_name:
        await query.answer("Siz ushbu nomzod uchun avval ovoz bergansiz!")
        return

    # Ovoz berishni saqlash
    candidates[candidate_name]['votes'] += 1
    user_votes[user_ip] = candidate_name

    await query.answer("Ovoz berildi!")
    await query.message.reply_text(f"{candidate_name} uchun ovoz berildi! Yangi ovozlar: {candidates[candidate_name]['votes']}")

# Botni ishga tushirish
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))
    app.add_handler(CallbackQueryHandler(vote_menu, pattern="vote_menu"))
    app.add_handler(CallbackQueryHandler(candidate_menu, pattern="^(Nomzod 1|Nomzod 2|Nomzod 3|Nomzod 4|Nomzod 5|Nomzod 6|Nomzod 7|Nomzod 8|Nomzod 9|Nomzod 10)$"))
    app.add_handler(CallbackQueryHandler(cast_vote, pattern="vote_.*"))
    app.run_polling()

if __name__ == '__main__':
    main()
