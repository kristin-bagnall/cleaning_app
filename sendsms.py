from twilio.rest import Client
import os

# Your Account SID from twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
# Your Auth Token from twilio.com/console
auth_token  = os.environ['TWILIO_AUTH_TOKEN']

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+18083830683", 
    from_="+14427776405",
    body="Hello from Kristin! I just set up my first API")

print(message.sid)

# repsonse: SM2fa0ab612a064f5d956e32b125f19207