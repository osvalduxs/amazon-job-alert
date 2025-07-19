import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def check_vacancy():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.jobsatamazon.co.uk/app#/jobSearch"
    driver.get(url)

    # Bandymas uždaryti cookies langą
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button/div[contains(text(),'Accept')]"))
        ).click()
    except:
        pass

    # Tikrinam ar rodo "job found"
    try:
        element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'job found')]"))
        )
        count_text = element.text.strip()
        print("Rasta:", count_text)
        driver.quit()
        return True, count_text
    except Exception as e:
        print("Nerasta darbo:", e)
        driver.quit()
        return False, "0 jobs"

def send_alert(location):
    subject = f"Amazon darbas: {location}"
    body = f"""Sveiki,\n\nRastas darbo skelbimas: {location}.\nPatikrink čia: https://www.jobsatamazon.co.uk/app#/jobSearch\n\nSėkmės!"""

    sender_email = "d62926000@gmail.com"
    receiver_email = "d62926000@gmail.com"
    password = os.getenv("EMAIL_PASSWORD")

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Laiškas išsiųstas sėkmingai!")
    except Exception as e:
        print(f"Nepavyko išsiųsti laiško: {e}")

if __name__ == "__main__":
    found, location = check_vacancy()
    if found:
        send_alert(location)
    else:
        print(f"Nerasta darbo skelbimų: {location}")
