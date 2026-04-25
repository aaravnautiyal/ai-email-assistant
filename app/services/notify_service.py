import requests
from app.config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def format_message(email, analysis):
    """Build a clean Telegram message from email + analysis."""

    # 🔥 Fallback summary
    summary = analysis.get("summary")
    if not summary or summary == "None":
        body = email.get("body", "")
        summary = body[:200] + "..." if len(body) > 200 else body

    # 🔗 Gmail link
    email_link = f"https://mail.google.com/mail/u/0/#inbox/{email.get('id')}"

    lines = []

    lines.append("🚨 *IMPORTANT PLACEMENT EMAIL*")
    lines.append(f"*From:* {email['sender']}")
    lines.append(f"*Subject:* {email['subject']}")
    lines.append("")

    lines.append(f"🏢 *Company:* {analysis.get('company', 'Not specified')}")
    lines.append(f"📊 *CGPA:* {analysis.get('cgpa', 'Not specified')}")
    lines.append(f"🎓 *Branches:* {analysis.get('branches', 'Not specified')}")
    lines.append(f"💰 *Stipend:* {analysis.get('stipend', 'Not specified')}")
    lines.append(f"📍 *Location:* {analysis.get('location', 'Not specified')}")
    lines.append(f"⏰ *Deadline:* {analysis.get('deadline', 'Not specified')}")

    lines.append("")
    lines.append(f"📝 *Summary:* {summary}")

    lines.append("")
    lines.append(f"🔗 [Open Email]({email_link})")

    return "\n".join(lines)


def send_telegram_notification(email, analysis):
    """Send a Telegram message for an important email."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  Telegram not configured — skipping notification")
        return False

    message = format_message(email, analysis)

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ Telegram sent: {email['subject'][:50]}")
            return True
        else:
            print(f"❌ Telegram error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Telegram exception: {e}")
        return False