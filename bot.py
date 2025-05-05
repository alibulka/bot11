from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# 🔐 Вставь свой токен от @BotFather
BOT_TOKEN = "7930196417:AAGFjnNmBtt41quSSZgv4E5RNUQi8-JyyR0"

# 📁 Папка, где лежат медиафайлы
MEDIA_FOLDER = "audio"

# 🎯 Список заданий по группам
GROUP_FILES = {
    "1": [
        {
            "photo": "photo1.jpg",
            "audio": "katya 1.ogg",
            "text": "📌 Katya, 23",
        },
         {
            
            "audio": "katya 1.ogg",
            "text": "1. How did you first come to realize or get diagnosed as autistic, and what was that process like for you?",
        },
       
    ],
    
    
}

# 📍 Обработка /start: меню выбора группы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1", callback_data="group_1")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! 👋\nВыберите номер :", reply_markup=reply_markup)

# 📍 Обработка выбора группы
async def group_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    group_number = query.data.split("_")[1]

    files = GROUP_FILES.get(group_number)
    if not files:
        await query.message.reply_text("Файлы для этой группы не найдены.")
        return

    for item in files:
        photo_path = os.path.join(MEDIA_FOLDER, f"group{group_number}", item["photo"])
        audio_path = os.path.join(MEDIA_FOLDER, f"group{group_number}", item["audio"])
        text = item.get("text", "")

        # Отправка фото с подписью
        try:
            with open(photo_path, "rb") as photo:
                await query.message.reply_photo(photo=photo, caption=text)
        except FileNotFoundError:
            await query.message.reply_text(f"❗ Фото не найдено: {item['photo']}")

        # Отправка аудио
        try:
            with open(audio_path, "rb") as audio:
                await query.message.reply_audio(audio=audio)
        except FileNotFoundError:
            await query.message.reply_text(f"❗ Аудио не найдено: {item['audio']}")

# 🚀 Запуск бота
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(group_selected))
    application.run_polling()
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
