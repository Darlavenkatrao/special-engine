import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Gemini AI API Configuration
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# బాట్ కేవలం టీవీ మెకానిక్‌గా మాత్రమే ప్రవర్తించేలా రూల్స్ సెట్ చేయడం
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
    user_text = update.message.text
    
    try:
        # AI ద్వారా సమాధానాన్ని జనరేట్ చేయడం
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("క్షమించండి, సమాధానం వెతకడంలో చిన్న సమస్య వచ్చింది. మళ్ళీ ప్రయత్నించండి.")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_message))
    
    print("TV Mechanic AI Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
