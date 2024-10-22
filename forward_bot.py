import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# enter bot token and group ID
TOKEN = '<token_id>'
GROUP_CHAT_ID = '<group_chat_id>'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bot is running!')

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        logger.info(f"Received message: {update.message.text}")
        # Check that msg was forwarded from channel
        if update.message.chat.type == 'channel':
            await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=update.message.text)

def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, forward_message))
    
    app.run_polling()

if __name__ == '__main__':
    main()
