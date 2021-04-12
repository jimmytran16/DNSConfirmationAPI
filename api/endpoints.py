from flask_restful import Resource, request
from . import app, api

from .twilio.send import send_comfirmation_text_msg_to_reciever

# Main endpoint
class Main(Resource):
    def get(self):
        return { 'message': 'Welcome to the Designer Nail Salon Messaging API' }

# Token Generator endpoint - generates JWT to the Designer Web App, to authorize use of AppointmentConfirmation 
class GenerateToken(Resource):
    def get(self):
        jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        return { 'success':'true', 'accessToken': jwt }

# Appointment Confirmation endpoint
class AppointmentConfirmation(Resource):
    def get(self):
        try:
            # retrieving args from the query url string from the request object
            args = request.args 
            print(args)
            # validate the args, make sure all required params are passed in from the request args
            if 'key' not in args or 'number' not in args or 'message' not in args:
                return { 'success':'false', 'message':'Missing params key, number, or message' }

            # call the send_comfirmation_text_msg_to_reciever function and pass in the args
            message_sid = send_comfirmation_text_msg_to_reciever(args['key'],args['number'],args['message'])
            return { 'success': 'true', 'message':'successfully confirmed {}'.format(message_sid) }
        
        except Exception as e: # handling error
            return { 'success': 'false', 'message':'unsuccessful comfirmed - {}'.format(e) }

api.add_resource(Main,'/')
api.add_resource(GenerateToken,'/getToken')
api.add_resource(AppointmentConfirmation, '/sendConfirmation')

