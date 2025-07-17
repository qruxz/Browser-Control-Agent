# 🧠 Browser Agent – AI-Powered Conversational Browser Automation

**Browser Agent** is a smart assistant that chats with you like a human and performs real-time browser actions — sending Gmail emails, doing Google searches, and responding naturally. Built as part of the **Banthry AI Challenge 2025**, this project uses browser automation, AI intent parsing, and Streamlit UI — all without using Gmail or Google APIs.

---

## 🚀 Features

- ✉️ **Gmail Email Sender (via Selenium)**  
  Automates composing and sending emails through Gmail using browser control  
  → Just ask: _"Send an email to Alice about the meeting"_  
  → Captures every step with screenshots

- 🔎 **Google Search Automation**  
  Performs a full Google search in a real browser tab  
  → Ask: _"Search for recent AI news on Google"_  
  → Returns screenshots of the results

- 🧠 **Conversational Chatbot (Groq + Regex)**  
  Not just commands — it chats like a person!  
  → Try: _"Tell me a joke"_ or _"What's your name?"_

- ✍️ **AI Email Generator (Groq API)**  
  Automatically writes smart email content when only a topic is given  
  → Uses Mixtral model from Groq for fast, context-rich text

- 📸 **Step-by-Step Screenshot Capture**  
  Takes screenshots of each browser action (e.g., open Gmail, type subject, send)  
  → Useful for debugging, transparency, and feedback

- 💬 **Streamlit Chat UI (GPT-style)**  
  Clean, modern interface with human-style bubbles  
  → Includes both user input and assistant replies with screenshot preview

---

## 🎥 Demo Preview
![Demo Screenshot](screenshots/final_demo_email_sent.png)

---

## 🧠 Tech Stack

| Layer            | Tools Used                                |
|------------------|--------------------------------------------|
| Frontend         | Streamlit + custom CSS for chat look      |
| Automation       | Selenium (browser control)                |
| AI Generation    | Groq API (Mixtral model)                  |
| Intent Parsing   | Regex-based basic NLP                     |
| Screenshotting   | Selenium full-page captures               |
| Config Handling  | dotenv for secrets like email/pass        |

---

## 🗂 Project Structure

Browser-Agent/
├── app.py               ← Streamlit UI + chat logic  
├── agent_controller.py ← Intent parsing + action handler  
├── browser_driver.py    ← Gmail + Google automation via Selenium  
├── content_generator.py ← Groq API-powered email generator  
├── screenshot_manager.py← Takes and stores screenshots  
├── utils.py             ← Helpers (regex parsing, validation)  
├── requirements.txt     ← All Python dependencies  
├── .env                 ← Secrets (email/password/Groq key)  
├── README.md            ← You’re reading it  
└── screenshots/         ← Step-by-step captured PNGs  



---

## ⚙️ Setup & Usage

```bash
# Clone the repo
git clone https://github.com/yourusername/browser-agent.git
cd browser-agent

# Create environment
python -m venv env
source env/bin/activate      # or .\env\Scripts\activate on Windows

# Install packages
pip install -r requirements.txt

# Add config to .env
echo EMAIL_ID=your_email@gmail.com >> .env
echo EMAIL_PASSWORD=your_password >> .env
echo GROQ_API_KEY=your_groq_key >> .env

# Run the app
streamlit run app.py
