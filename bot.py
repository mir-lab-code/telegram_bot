from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from util import load_prompt

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = load_prompt('random')



app = ApplicationBuilder().token("7602773018:AAF8N9lotSt3aNp-ESFG26hmYCWn5uGeln4").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
app.run_polling()