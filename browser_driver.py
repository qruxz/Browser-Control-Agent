from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from screenshot_manager import take_screenshot
import time

# --- ✉️ SEND EMAIL via Gmail ---
def send_email(state):
    email = state["email"]
    password = state["password"]
    recipient = state["recipient"]
    subject = state["subject"]
    body = state["body"]

    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://mail.google.com/")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "identifierId")))
        take_screenshot(driver, "email_gmail_login")

        # --- Enter Email ---
        driver.find_element(By.ID, "identifierId").send_keys(email + Keys.RETURN)
        time.sleep(3)

        # --- Enter Password ---
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
        time.sleep(5)

        # --- Compose Email ---
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".T-I.T-I-KE.L3"))).click()
        time.sleep(2)
        take_screenshot(driver, "email_gmail_compose")

        # --- Fill Fields ---
        driver.find_element(By.NAME, "to").send_keys(recipient)
        driver.find_element(By.NAME, "subjectbox").send_keys(subject)
        driver.find_element(By.CSS_SELECTOR, "div[aria-label='Message Body']").send_keys(body)
        take_screenshot(driver, "email_gmail_ready_to_send")

        # --- Send Email ---
        driver.find_element(By.CSS_SELECTOR, "div[aria-label*='Send'][role='button']").click()
        time.sleep(2)
        take_screenshot(driver, "email_gmail_sent")

        return "screenshots/email_gmail_sent.png"

    except Exception as e:
        print("Gmail Error:", e)
        take_screenshot(driver, "email_gmail_error")
        return "screenshots/email_gmail_error.png"

    finally:
        driver.quit()

# --- 🔍 Google Search Automation ---
def perform_google_search(state):
    query = state["query"]

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.google.com/")
        time.sleep(2)
        take_screenshot(driver, "google_home")

        driver.find_element(By.NAME, "q").send_keys(query + Keys.RETURN)
        time.sleep(3)
        take_screenshot(driver, "google_results")

        return "screenshots/google_results.png"

    except Exception as e:
        print("Search Error:", e)
        take_screenshot(driver, "google_search_error")
        return "screenshots/google_search_error.png"

    finally:
        driver.quit()
