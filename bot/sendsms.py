from twilio.rest import Client

account_sid = "ACe03cfbd8cafd6cb24efcbb52bac439f4"
auth_token = "d082865f9660eacff99e339377e8faaa"

def send(message):
    """Sends SMS message via Twilio API"""
    client = Client(account_sid, auth_token)
    client.messages.create(
    to="+919747203442",
    from_="+15207627955",
    body=message)
