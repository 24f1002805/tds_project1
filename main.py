import os
import json
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

app = FastAPI()

TELEGRAM_TOKEN = "8952277673:AAHKiU_I-cO1dtLllLef_t5-f1Go3Wai2JQ"
RENDER_URL = os.getenv("RENDER_URL", "https://your-app-name.onrender.com")

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Logic placeholder for analysis answer
    analysis_answer = {"result": "Analyzed question successfully"}

    log_data = {"question": user_message, "answer": analysis_answer, "status": "SUCCESS"}
    with open("run.jsonl", "w") as f:
        f.write(json.dumps(log_data) + "\n")

    final_response = {
        "answer": analysis_answer,
        "log_url": f"{RENDER_URL}/run.jsonl"
    }

    await update.message.reply_text(json.dumps(final_response))

application = Application.builder().token(TELEGRAM_TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.get("/run.jsonl")
def get_log():
    if os.path.exists("run.jsonl"):
        with open("run.jsonl", "r") as f:
            return f.read()
    return "{}"

@app.on_event("startup")
async def startup_event():
    await application.initialize()
    webhook_url = f"{RENDER_URL}/webhook"
    await application.bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
