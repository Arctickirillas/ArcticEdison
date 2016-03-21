from twilio.rest import TwilioRestClient

account = "AC74f6a665ac3dde20a3c255e725d0f968"
token = "9093817ec2565332e48471d591be54d9"
client = TwilioRestClient(account, token)

def sendSMS(number = "+79601825839"):
    message = client.messages.create(to=number, from_= "+12034799526",
                                     body="ATTENTION!!! PARTY HARD!!!")
# Example
#sendSMS()