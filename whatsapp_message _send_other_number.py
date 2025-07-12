from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load secrets from .env
load_dotenv()

# Get Twilio credentials & numbers from env
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH')
twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_FROM')
to_whatsapp_number = os.getenv('TWILIO_WHATSAPP_TO')

# Create client
client = Client(account_sid, auth_token)

# Send message
try:
    message = client.messages.create(
        body='Hello from Python using Twilio WhatsApp API!',
        from_=twilio_whatsapp_number,
        to=to_whatsapp_number
    )
    print("✅ Message sent successfully. SID:", message.sid)

except Exception as e:
    print("❌ Failed to send message:", str(e))
