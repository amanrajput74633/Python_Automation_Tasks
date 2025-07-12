from mailjet_rest import Client
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

api_key = os.getenv('MAILJET_API_KEY')
api_secret = os.getenv('MAILJET_API_SECRET')

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

data = {
  'Messages': [
    {
      "From": {
        "Email": "rajputaman74633@gmail.com",
        "Name": "Anonymous Sender"
      },
      "To": [
        {
          "Email": "amanrajput74633@gmail.com",
          "Name": "Receiver"
        }
      ],
      "Subject": "testing purpose",
      "TextPart": "This is an anonymous email using Mailjet and Python.",
    }
  ]
}

result = mailjet.send.create(data=data)

print(result.status_code)
print(result.json())
