import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai
import wikipedia
from langdetect import detect
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

# ✅ Support Group Link
SUPPORT_GROUP_LINK = "https://t.me/+H4TLyLB0TBM0NzY9"

async def support(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("🔗 Join Support Group", url=SUPPORT_GROUP_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚡ **Need Help? Join our Support Group!**", reply_markup=reply_markup)

# 🔹 OpenAI API Key Set करना
openai.api_key = OPENAI_KEY

# 🛠 **Logging सेटअप**
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🌐 **Dynamic Language Detection**
def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return "en"

# 🔥 **Smart Reply System**
def smart_reply(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    lang = detect_language(text)
    
    if "arshid" in text.lower():  # 👑 Owner Toxic (Arshid) का नाम आया
        response = f"🔥🔥 {update.message.from_user.first_name}, Arshid के बारे में सही बोलो!"
    else:
        response = "🤖 मैं यहाँ हूँ! क्या मदद कर सकता हूँ?"

    update.message.reply_text(response)

# ✅ **Start Command**
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("👥 Join Group", url=GROUP_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 **Welcome to Toxic Bot!**\n\n"
        "🔥 मैं आपके लिए हर सवाल का जवाब दे सकता हूँ।\n"
        "ℹ️ **Commands:** /help, /group, /ask\n"
        "📌 **Owner:** Arshid\n\n"
        "👉 **Join Group for More!**",
        reply_markup=reply_markup
)
  # 🛠 **Help Command**
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "**📌 Available Commands:**\n\n"
        "🔹 /group - सभी ग्रुप मैनेजमेंट कमांड्स\n"
        "🔹 /wiki <query> - विकिपीडिया सर्च\n"
        "🔹 /ask <question> - AI से सवाल पूछें\n"
        "🔹 /mentionall - सभी सदस्यों को टैग करें\n"
        "🔹 /afk <reason> - AFK मोड सेट करें\n"
        "🔹 /info <username> - किसी भी यूजर की जानकारी लें"
    )

# 🌐 **Wikipedia Search**
async def wiki_command(update: Update, context: CallbackContext) -> None:
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("❌ कृपया /wiki के बाद एक विषय लिखें।")
        return

    try:
        summary = wikipedia.summary(query, sentences=2, auto_suggest=False)
        await update.message.reply_text(f"📚 **Wikipedia Result for:** {query}\n\n{summary}")
    except:
        await update.message.reply_text("❌ कोई परिणाम नहीं मिला।")

# 🚀 **AI Chat System (Ask Command)**
async def ask_command(update: Update, context: CallbackContext) -> None:
    question = " ".join(context.args)
    if not question:
        await update.message.reply_text("❌ कृपया /ask के बाद एक सवाल लिखें।")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        reply = response["choices"][0]["message"]["content"].strip()
        await update.message.reply_text(f"🤖 **AI Response:**\n{reply}")
    except Exception as e:
        await update.message.reply_text("⚠️ AI से जवाब लाने में दिक्कत हो रही है।")

# ✅ **Main Function**
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # 🔹 Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("wiki", wiki_command))
    app.add_handler(CommandHandler("ask", ask_command))

    # 🔹 Message Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))

    # 🔥 **Start Bot**
    print("🚀 Toxic Bot is Running!")
    app.run_polling()

if __name__ == "__main__":
    main()
