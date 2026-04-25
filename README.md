# 🤖 AI Email Assistant (Gmail + Gemini + Telegram)

An AI-powered system that automatically reads your Gmail inbox, identifies important job/internship emails, extracts key details, and sends real-time alerts to your phone via Telegram.

---

## 🚀 Features

- 📧 Reads unread Gmail emails using Gmail API
- 🧠 Uses Gemini AI to:
  - Detect important emails
  - Extract structured info (company, CGPA, stipend, etc.)
- 📲 Sends alerts via Telegram bot
- 🔄 Runs automatically (scheduler)
- ✅ Marks emails as read after processing
- 🔗 Includes direct Gmail link in notification
- 🧾 Fallback summary if AI fails

---

## 🧠 Tech Stack

- Python
- Gmail API (OAuth)
- Google Gemini API
- Telegram Bot API
- APScheduler

---

## ⚙️ Setup

1. Clone repo:
bash
git clone https://github.com/aaravnautiyal/ai-email-assistant.git
cd ai-email-assistant

2. Create .env
GEMINI_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id

3.Install dependencies - 
pip install -r requirements.txt

4.Run - python -m app.main

5. Example output - 
   
   
   🚨 IMPORTANT PLACEMENT EMAIL

🏢 Company: Dyson
📊 CGPA: Not specified
💰 Stipend: Not specified
📍 Location: Not specified

📝 Summary:
Dyson is hiring interns...

🔗 Open Email



