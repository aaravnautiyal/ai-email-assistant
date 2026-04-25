import json
import google.generativeai as genai
from app.config.settings import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_email(subject, body):
    """Send email to Gemini and return structured analysis."""

    prompt = f"""
    You are an AI system that extracts structured information from placement and internship emails.

    IMPORTANT RULE:
    If the email is about jobs, internships, or hiring → mark as IMPORTANT.

    Extract the following fields:
    - Company name (VERY IMPORTANT – infer from subject if needed)
    - CGPA requirement (write "No requirement" if not mentioned)
    - Eligible branches
    - Eligibility (BTech, etc.)
    - Stipend (write "Not specified" if missing)
    - Location (write "Not specified" if missing)
    - Deadline (write "Not specified" if missing)

    ⚠️ DO NOT leave fields empty. Always fill with:
    - "Not specified" OR "No requirement"

    Return ONLY valid JSON:

    {{
    "importance": "IMPORTANT or NOT IMPORTANT",
    "company": "...",
    "cgpa": "...",
    "branches": "...",
    "eligibility": "...",
    "stipend": "...",
    "location": "...",
    "deadline": "...",
    "summary": "short summary including company + role"
    }}

    Email:
    Subject: {subject}
    Body: {body}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text

        return parse_response(text)

    except Exception as e:
        return {
            "importance": "NOT IMPORTANT",
            "company": None,
            "cgpa": None,
            "branches": None,
            "eligibility": None,
            "stipend": None,
            "location": None,
            "deadline": None,
            "summary": None,
            "raw": f"Error: {str(e)}"
        }


def parse_response(text):
    """Extract JSON safely from LLM output"""
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        json_str = text[start:end]
        return json.loads(json_str)

    except Exception as e:
        print("Parsing failed:", e)
        return {
            "importance": "NOT IMPORTANT",
            "summary": text
        }


def force_importance(email, result):
    """Rule-based fallback to ensure important emails are not missed"""

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

def fix_missing_fields(email, result):
    subject = email["subject"]

    # Try extracting company from subject if missing
    if not result.get("company") or result["company"] == "Not specified":
        words = subject.split()
        result["company"] = words[0]  # simple heuristic

    return result