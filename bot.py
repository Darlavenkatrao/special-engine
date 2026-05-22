import os
import threading
from flask import Flask
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Render కోసం డమ్మీ వెబ్ సర్వర్ క్రియేట్ చేయడం
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    # Render ఇచ్చే Port ని తీసుకుంటుంది
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# Gemini AI API Configuration
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

SYSTEM_PROMPT = """
You are an expert LED/LCD TV Repair Technician and Consultant. 
Your job is to help TV mechanics in a Telegram group with technical advice, tips, motherboard voltages, LED TV panel voltages, and T-Con board problems.
Respond in the SAME language the user asks the question (e.g., if asked in Telugu, reply in Telugu; if in Hindi, reply in Hindi).
Keep answers highly technical, helpful, and accurate for mechanics. If a question is NOT related to TV repair or electronics, politely say that you can only help with TV repair queries.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
        
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("క్షమించండి, సమాధానం వెతకడంలో చిన్న సమస్య వచ్చింది. మళ్ళీ ప్రయత్నించండి.")

def main():
    # వెబ్ సర్వర్‌ను బ్యాక్‌గ్రౌండ్‌లో రన్ చేయడం
    threading.Thread(target=run_flask, daemon=True).start()

    TOKEN = os.getenv("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_message))
    
    print("TV Mechanic AI Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
