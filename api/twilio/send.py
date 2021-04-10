from twilio.rest import Client
import os

#development imports
from dotenv import load_dotenv
load_dotenv()

# function to send out the confirmation text message
def send_comfirmation_text_msg_to_reciever(key,reciever,body):
    # validate if the auth key is valid before proceeding
    if key != os.getenv('CONFIRMATION_API_KEY'): 
        raise ValueError('Invalid authentication key')
    else:
        # Your Account SID from twilio.com/console
        account_sid = os.getenv('ACCOUNT_SID')
        # Your Auth Token from twilio.com/console
        auth_token  = os.getenv('AUTH_TOKEN')

        client = Client(account_sid, auth_token)

        trail_number = '+1{}'.format(os.getenv('SENDER_NUMBER'))
        reciever_number = '+1{}'.format(reciever)

        print(reciever_number,trail_number,body)
        # Send the message to the client
        message = client.messages.create(
            to=reciever_number, 
            from_=trail_number,
            body=body)

        return message.sid

if __name__ == '__main__':
    try:
        send_comfirmation_text_msg_to_reciever('123',77777777777,'hi')
    except Exception as e:
        print('unable to send the message {}'.format(e))
