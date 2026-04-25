from app.services.gmail_service import get_unread_emails
from app.services.llm_service import analyze_email, fix_missing_fields
from app.services.notify_service import send_telegram_notification


# 🔥 Safety override (rule-based importance)
def force_importance(email, result):
    text = (email["subject"] + email["body"]).lower()

    keywords = [
        "intern", "internship",
        "job", "placement",
        "hiring", "apply",
        "deadline", "recruitment"
    ]

    if any(k in text for k in keywords):
        result["importance"] = "IMPORTANT"

    return result


def main():
    print("🚀 Starting Email AI Agent...\n")

    try:
        emails = get_unread_emails()

        if not emails:
            print("📭 No new emails found.")
            return

        for email in emails:
            print("\n📧 Processing Email")
            print("From:", email.get("sender"))
            print("Subject:", email.get("subject"))

            # 🧠 Analyze using LLM
            result = analyze_email(email["subject"], email["body"])

            # 🔥 Force importance
            result = force_importance(email, result)
            result = fix_missing_fields(email, result)

            print("🧠 AI Result:", result)

            # 🎯 Decision
            if result.get("importance") == "IMPORTANT":
                print("✅ Marked IMPORTANT → Sending Telegram")

                # ✅ FIXED CALL
                response = send_telegram_notification(email, result)

                print("📲 Telegram Response:", response)
            else:
                print("⏭️ Skipped (Not Important)")

    except Exception as e:
        print("❌ Error occurred:", str(e))


if __name__ == "__main__":
    main()