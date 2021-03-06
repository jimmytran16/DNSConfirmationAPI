from twilio.rest import Client
import os
from api.services.token.token_service import TokenizerService
from api.helpers.helpers import remove_non_numerical_char_from_phone_number

#development imports
from dotenv import load_dotenv
load_dotenv()

class TwilioService:

    def __init__(self):
        self.signature = os.getenv('SIGNATURE')
         # Your Account SID from twilio.com/console
        self.account_sid = os.getenv('ACCOUNT_SID')
        # Your Auth Token from twilio.com/console
        self.auth_token  = os.getenv('AUTH_TOKEN')
        self.sender_number = os.getenv('SENDER_NUMBER')
        self.admin_number = os.getenv('ADMIN_NUMBER')
        self.__tokenizer_service = TokenizerService()
    
    # function to send the appointment information to the admin's phone
    def send_appointment_info_to_admin(self, messageInfo):
        print(messageInfo)
        # If the body does not contain anything then we want don't want to send out the message
        if not messageInfo:
            return

        body = self.__create_body(messageInfo)

        try:
            client = Client(self.account_sid, self.auth_token)

            trail_number = '+1{}'.format(self.sender_number)
            reciever_number = '+1{}'.format(self.admin_number)

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


    # function to send out the confirmation text message
    def send_comfirmation_text_msg_to_reciever(self,key,reciever,body):
        reciever = remove_non_numerical_char_from_phone_number(reciever)
        try:
            # validate the JWT
            self.__tokenizer_service.authenticate_JWT(key,self.signature) 
           

            client = Client(self.account_sid, self.auth_token)

            trail_number = '+1{}'.format(self.sender_number)
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
    
    def __create_body(self, messageInfo):
        return '''
            REQUEST DATE: {} \n\nName: {} \n\nPhone Numer: {} \n\nEmail: {} \n\nTime: {} \n\nMessage: {} \n\nConfirmation Link: {}
        '''.format(messageInfo['date'],messageInfo['name'],messageInfo['phone'],messageInfo['email'],messageInfo['appointment'],messageInfo['message'],messageInfo['confirmationUrl'])
    

if __name__ == '__main__':
    try:
        _twilio_service = TwilioService()
        _twilio_service.send_comfirmation_text_msg_to_reciever('123',77777777777,'hi')
    except Exception as e:
        print('unable to send the message {}'.format(e))
