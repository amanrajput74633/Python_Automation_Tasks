from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Get credentials from environment
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH')
twilio_number = os.getenv('TWILIO_FROM')
target_number = os.getenv('TWILIO_TO')

# TwiML
twiml_url = 'http://demo.twilio.com/docs/voice.xml'

# Create Twilio client and make call
client = Client(account_sid, auth_token)

call = client.calls.create(
    url=twiml_url,
    to=target_number,
    from_=twilio_number
)

print(f"Call initiated. SID: {call.sid}")
