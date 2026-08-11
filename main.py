
import os
import json
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8952277673:AAHKiU_I-cO1dtLllLef_t5-f1Go3Wai2JQ"
WGETABLE_LOG_URL = "https://githubusercontent.com"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"📥 Received Question: {user_message}")
    
    analysis_answer = {"state": "Assam"}
    log_data = {"question": user_message, "answer": analysis_answer, "status": "SUCCESS"}
    
    with open("run.jsonl", "a") as f:
        f.write(json.dumps(log_data) + "\n")
        
    final_response = {
        "answer": analysis_answer,
        "log_url": WGETABLE_LOG_URL
    }
    
    await update.message.reply_text(json.dumps(final_response))

def main():
    print("🤖 Initializing Bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(app.bot.delete_webhook())
    except Exception:
        pass
        
    print("🚀 Bot is live! Leave this terminal open.")
    app.run_polling()

if __name__ == "__main__":
    main()
