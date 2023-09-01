import requests

def send_google_chat_message(webhook_url, message):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
    }
    payload = {
        'text': message,
    }
    response = requests.post(webhook_url, json=payload, headers=headers)
    return response.status_code == 200



#Setting up twilio for msg service
from twilio.rest import Client

def send_sms_reminder(account_sid, auth_token, to_phone_number, from_phone_number, message):
    client = Client(account_sid, auth_token)
    client.messages.create(to=to_phone_number, from_=from_phone_number, body=message)


