import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get credentials and email info
sender_email = os.getenv("GMAIL_EMAIL")
receiver_email = os.getenv("GMAIL_RECEIVER")
password = os.getenv("GMAIL_PASSWORD")

subject = "Hello from Python"
body = "Hi Aman, this is a test email sent using Python."

# Create email
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content(body)

# Send email via Gmail
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, password)
    smtp.send_message(msg)

print("✔ Email sent successfully!")
