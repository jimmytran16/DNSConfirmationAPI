from flask_restful import Resource, request
from flask import jsonify
from . import app, api
from .twilio.send import send_comfirmation_text_msg_to_reciever
from .token.tokenizer import generate_JWT

# Main endpoint
class Main(Resource):
    def get(self):
        return jsonify({ 'message': 'Welcome to the Designer Nail Salon Messaging API' })

# Token Generator endpoint - generates JWT to the Designer Web App, to authorize use of AppointmentConfirmation 
class GenerateToken(Resource):
    def get(self):
        try:
            # retrieve api token from the client
            apiKey = request.args['apiKey']
            token = generate_JWT(apiKey).decode("utf-8")
            response = { 'success':True, 'accessToken': token } 
            return jsonify(response)
        except Exception as e:
            print('generate exception ',e)
            response = { 'success':False, 'accessToken': 'error_generating_token' + str(e).replace(' ','_') }
            return jsonify(response)

# Appointment Confirmation endpoint
class AppointmentConfirmation(Resource):
    def get(self):
        try:
            # retrieving args from the query url string from the request object
            args = request.args 
            # validate the args, make sure all required params are passed in from the request args
            if 'key' not in args or 'number' not in args or 'message' not in args:
                response = { 'success':'false', 'message':'Missing params key, number, or message' }
                return jsonify(response)

            # call the send_comfirmation_text_msg_to_reciever function and pass in the args
            message_sid = send_comfirmation_text_msg_to_reciever(args['key'],args['number'],args['message'])
            response = { 'success': True, 'message':'successfully confirmed {}'.format(message_sid) }
            return jsonify(response)
        
        except Exception as e: # handling error
            response = { 'success': False, 'message':'unsuccessful comfirmed - {}'.format(e) }
            return jsonify(response)

api.add_resource(Main,'/')
api.add_resource(GenerateToken,'/getToken')
api.add_resource(AppointmentConfirmation, '/sendConfirmation')

