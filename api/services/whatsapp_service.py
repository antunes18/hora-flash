import os
from typing import List, Tuple

try:
    from twilio.rest import Client
except ImportError:
    Client = None

class WhatsAppService:
    def __init__(self):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        if Client and account_sid and auth_token and self.from_number:
            self.client = Client(account_sid, auth_token)
        else:
            self.client = None

    def send_message(self, to_number: str, message: str):
        """
        Send a single WhatsApp message. Uses Twilio API if configured, otherwise falls back to pywhatkit.
        """
        if self.client:
            self.client.messages.create(
                body=message,
                from_=f"whatsapp:{self.from_number}",
                to=f"whatsapp:{to_number}"
            )
        else:
            import pywhatkit
            # Instant send without opening new tabs repeatedly; pywhatkit handles session reuse
            pywhatkit.sendwhatmsg_instantly(to_number, message, wait_time=10)

    def send_bulk(self, messages: List[Tuple[str, str]]):
        """
        Send multiple messages in sequence without opening new browser tabs for each.
        """
        for to, msg in messages:
            self.send_message(to, msg)