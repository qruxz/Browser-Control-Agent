
from content_generator import generate_email_content
import re

# --- 🔁 Global State to Track Flow ---
state = {
    "mode": None,        # "email" or "google"
    "email": None,
    "password": None,
    "recipient": None,
    "subject": None,
    "body": None,
    "dates": None,
    "query": None
}

# --- 🔍 Intent-Based Handler ---
def handle_user_input(user_input):
    global state

    # --- Detect Mode First ---
    if state["mode"] is None:
        if "email" in user_input.lower() or "mail" in user_input.lower():
            state["mode"] = "email"
            return "Sure! What is your Gmail address?", state
        elif "search" in user_input.lower() or "google" in user_input.lower():
            state["mode"] = "google"
            query = extract_search_query(user_input)
            if query:
                state["query"] = query
                return f"Got it. Searching for '{query}' on Google...", state
            return "What would you like me to search on Google?", state
        else:
            return "Do you want to send an email or search something on Google?", state

    # --- Google Mode ---
    if state["mode"] == "google":
        if not state["query"]:
            state["query"] = extract_search_query(user_input) or user_input
            return f"Searching for '{state['query']}'...", state
        return "Launching browser to search now...", state

    # --- Email Mode ---
    if state["mode"] == "email":

        if not state["email"]:
            email = extract_email(user_input)
            if email:
                state["email"] = email
                return "✅ Email saved. What is your Gmail password?", state
            return "❗Please provide a valid Gmail address.", state

        if not state["password"]:
            state["password"] = user_input.strip()
            return "Who is the recipient of this email?", state

        if not state["recipient"]:
            email = extract_email(user_input)
            if email:
                state["recipient"] = email
                return "What is the email about?", state
            return "Please provide a valid recipient email address.", state

        if not state["dates"]:
            extracted_date = extract_date(user_input)
            if extracted_date:
                state["dates"] = extracted_date  # store it, even if we don't use it now
                return "Got the date. What should the email say?", state

        if not state["subject"] or not state["body"]:
            subject, body = generate_email_content({**state, "raw_input": user_input})
            state["subject"] = subject
            state["body"] = body
            return "📤 Preparing to send the email now...", state

        return "✅ Email ready to be sent. Launching browser...", state

    return "Hmm... I'm not sure what to do next.", state

# --- 🧠 Regex Extractors ---
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_search_query(text):
    cleaned = re.sub(r"(search|google|for|about|on)\s*", "", text, flags=re.IGNORECASE)
    return cleaned.strip() if cleaned else None

def extract_date(text):
    # Simple keywords and date-like strings
    date_keywords = ["today", "tomorrow", "next week", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for word in date_keywords:
        if word in text.lower():
            return word.capitalize()

    # Check for formats like July 20, 20th July, etc.
    match = re.search(r'\b(?:\d{1,2}(st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2})\b', text, re.IGNORECASE)
    return match.group(0) if match else None
