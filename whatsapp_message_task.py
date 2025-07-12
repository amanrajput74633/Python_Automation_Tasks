import pywhatkit as kit
import datetime
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Get number from environment
phone_number = os.getenv("WHATSAPP_NUMBER")

# Message to send
message = "Hello! This message was sent using Python 🤖"

# Time setup
now = datetime.datetime.now()
hour = now.hour
minute = now.minute + 1

# Send message
try:
    kit.sendwhatmsg(phone_number, message, hour, minute)
    print("✅ WhatsApp message scheduled successfully!")
except Exception as e:
    print("❌ Error:", e)
