from app.services.gmail_service import get_gmail_service

if __name__ == "__main__":
    service = get_gmail_service()
    print("✅ Gmail authenticated successfully!")