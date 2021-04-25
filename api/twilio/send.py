from twilio.rest import Client
import os
from api.token.tokenizer import authenticate_JWT
from api.helpers.helpers import remove_non_numerical_char_from_phone_number

#development imports
from dotenv import load_dotenv
load_dotenv()

# function to send out the confirmation text message
def send_comfirmation_text_msg_to_reciever(key,reciever,body):
    signature = os.getenv('SIGNATURE')
    reciever = remove_non_numerical_char_from_phone_number(reciever)
    try:
        # validate the JWT
        authenticate_JWT(key,signature) 
        # Your Account SID from twilio.com/console
        account_sid = os.getenv('ACCOUNT_SID')
        # Your Auth Token from twilio.com/console
        auth_token  = os.getenv('AUTH_TOKEN')

        client = Client(account_sid, auth_token)

        trail_number = '+1{}'.format(os.getenv('SENDER_NUMBER'))
        reciever_number = '+1{}'.format(reciever)

        # Send the message to the client
        message = client.messages.create(
            to=reciever_number, 
            from_=trail_number,
            body=body)

        # return message.sid

        # this return is for testing purposes - to test the functions content 
        return { 'sid':message.sid, 'from':trail_number, 'to':reciever_number, 'body':body }   
    except Exception as e:
        raise Exception(str(e))
    
if __name__ == '__main__':
    try:
        send_comfirmation_text_msg_to_reciever('123',77777777777,'hi')
    except Exception as e:
        print('unable to send the message {}'.format(e))
