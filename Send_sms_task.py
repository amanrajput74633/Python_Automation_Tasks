from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load secrets from .env file
load_dotenv()

# Get credentials from environment
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH')
from_number = os.getenv('TWILIO_FROM')
to_number = os.getenv('TWILIO_TO')

# Create Twilio client and send message
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Hello Aman! This is a message from Twilio.",
    from_=from_number,
    to=to_number
)

print(f"✔ Message sent. SID: {message.sid}")
