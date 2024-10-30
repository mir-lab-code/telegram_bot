from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from util import load_prompt, load_message, send_image, send_text, Dialog, show_main_menu, send_text_buttons, default_callback_handler
from gpt import ChatGptService
from credentials import ChatGPT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'main'
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Главное меню',
        'random': 'Узнать случайный интересный факт 🧠',
        'gpt': 'Задать вопрос чату GPT 🤖',
        'talk': 'Поговорить с известной личностью 👤',
        'quiz': 'Поучаствовать в квизе ❓'
        # Добавить команду в меню можно так:
        # 'command': 'button text'
    })

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if dialog.mode == 'gpt':
        await gpt_dialod(update, context)
    elif dialog.mode == 'talk':
        await talk_dialog(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = load_prompt('random')
    message = load_message('random')

    await send_image(update, context, 'random')
    # message = await send_text(update, context, message)
    answer = await chat_gpt.send_question(prompt, '')
    # await message.edit_text(answer)
    await send_text_buttons(update, context, answer, {
        'random_more': 'Хочу еще рандомный факт',
        'random_end': 'Выйти из режима GPT'
    })

async def random_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    cb = update.callback_query.data
    if cb == 'random_more':
        await send_text(update, context, 'Нажмите /random')
    else:
        await send_text(update, context, 'Нажмите /start')

async def gpt(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'gpt'
    prompt = load_prompt('gpt')
    message = load_message('gpt')
    chat_gpt.set_prompt(prompt)
    await send_image(update, contex, 'gpt')
    await send_text(update, contex, message)

async def gpt_dialod(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    message = await send_text(update, contex, 'Думаю над вопросом...')
    answer = await chat_gpt.add_message(text)
    await message.edit_text(answer)

async def talk(update: Update, context:ContextTypes.DEFAULT_TYPE):
    dialog.mode = 'talk'
    message = load_message('talk')
    await send_image(update, context, 'talk')
    await send_text_buttons(update, context, message, {
        'talk_cobain': 'Курт Кобейн',
        'talk_queen': 'Елизавета II',
        'talk_tolkien': 'Джон Толкиен',
        'talk_nietzsche': 'Фридрих Ницше',
        'talk_hawking': 'Стивен Хокинг'
    })

async def talk_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    cb = update.callback_query.data
    prompt = load_prompt(cb)
    chat_gpt.set_prompt(prompt)
    answer = await chat_gpt.send_question(prompt, '')
    await send_image(update, context, cb)
    await send_text(update, context, answer)

async def talk_dialog(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    message = await send_text(update, contex, 'Думаю над вопросом...')
    answer = await chat_gpt.add_message(text)
    await message.edit_text(answer)



dialog = Dialog()
dialog.mode = None

chat_gpt = ChatGptService(ChatGPT_TOKEN)
app = ApplicationBuilder().token("7602773018:AAF8N9lotSt3aNp-ESFG26hmYCWn5uGeln4").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("talk", talk))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

app.add_handler(CallbackQueryHandler(random_button, pattern='^random_.*'))
app.add_handler(CallbackQueryHandler(talk_button, pattern='^talk_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()