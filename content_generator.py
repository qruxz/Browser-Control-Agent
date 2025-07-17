import os
from dotenv import load_dotenv
from groq import Groq

# --- 🔐 Load API Key ---
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# --- ✉️ Basic Email Content Generator ---
def generate_email_content(state):
    prompt = f"""
Write a formal, professional leave application email addressed to {state['recipient']}.

Include the following:
- Leave dates: {state['dates']}
- Reason: personal
- Sender: {state['email']}
Generate both:
1. Subject line
2. Full email body
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes professional emails."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content
    subject = "Leave Application for Personal Reasons"
    body = content

    # 🧠 Try extracting better subject from AI response
    if "Subject:" in content:
        parts = content.split("Subject:")
        if len(parts) > 1:
            subject_block = parts[1].split("\n")[0].strip()
            subject = subject_block
            body = "\n".join(parts[1].split("\n")[1:]).strip()

    return subject, body

# --- ✨ Smart Email Suggestions ---
def generate_smart_recommendations(user_instruction):
    full_prompt = f"""
You are a professional email-writing assistant.

Based on the following instruction, generate:
1. Three subject line suggestions
2. A more polished version of the email body
3. Two signature line suggestions

Instruction: "{user_instruction}"

Format your response like:
Subject Suggestions:
- ...
- ...
- ...

Improved Body:
...

Signature Suggestions:
- ...
- ...
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a smart professional email generator."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7
    )

    raw = response.choices[0].message.content

    # 🧪 Parse the structured output
    suggestions = {
        "subjects": [],
        "body": "",
        "signatures": []
    }

    try:
        if "Subject Suggestions:" in raw:
            sub_block = raw.split("Subject Suggestions:")[1].split("Improved Body:")[0]
            suggestions["subjects"] = [line.strip("-• ").strip() for line in sub_block.strip().split("\n") if line.strip()]

        if "Improved Body:" in raw:
            body_block = raw.split("Improved Body:")[1].split("Signature Suggestions:")[0].strip()
            suggestions["body"] = body_block

        if "Signature Suggestions:" in raw:
            sign_block = raw.split("Signature Suggestions:")[1]
            suggestions["signatures"] = [line.strip("-• ").strip() for line in sign_block.strip().split("\n") if line.strip()]
    except Exception:
        suggestions["body"] = raw  # fallback to raw output if format fails

    return suggestions
