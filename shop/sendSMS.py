# twilio_utils.py
from twilio.rest import Client
import os
def send_sms(to, body):
    try:
        client = Client(os.environ.get('TWILIO_ACCOUNT_SID'),os.environ.get('TWILIO_AUTH_TOKEN'))
        message = client.messages.create(
            to=to,
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            body=body
        )
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False