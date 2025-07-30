from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd

# Загрузка Excel-файла
df = pd.read_excel('переводчик артикулов новый.xlsx', engine='openpyxl')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь артикул, и я пришлю ссылку на товар на Wildberries."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # Поиск в столбце D
    match_d = df[df['D'].astype(str).str.strip() == user_input]
    # Поиск в столбце N
    match_n = df[df['N'].astype(str).str.strip() == user_input]

    if not match_d.empty:
        wb_id = str(match_d.iloc[0]['H']).strip()
        link = f"https://www.wildberries.ru/catalog/{wb_id}/detail.aspx?targetUrl=GP"
        await update.message.reply_text(f"Вот ссылка на товар:\n{link}")
    elif not match_n.empty:
        wb_id = str(match_n.iloc[0]['H']).strip()
        link = f"https://www.wildberries.ru/catalog/{wb_id}/detail.aspx?targetUrl=GP"
        await update.message.reply_text(f"Вот ссылка на товар:\n{link}")
    else:
        await update.message.reply_text("Артикул не найден.")

def main():
    # ВСТАВЬ свой токен сюда
    TOKEN = "8343960855:AAECX5APeXKEideED1j0BVWsx19VJkj_89w"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()