from flask_restful import Resource, request
from flask import jsonify
from api import app, api
from api.services.twilio.twilio_service import TwilioService
from api.services.token.token_service import TokenizerService

# Main endpoint
class Main(Resource):
    def get(self):
        return jsonify({ 'message': 'Welcome to the Designer Nail Salon Confirmation API' })

# Token Generator endpoint - generates JWT to the Designer Web App, to authorize use of AppointmentConfirmation 
class GenerateToken(Resource):
    def __init__(self):
        self._tokenizer_service = TokenizerService()

    def get(self):
        try:
            # retrieve api token from the client
            apiKey = request.args['apiKey']
            token = self._tokenizer_service.generate_JWT(apiKey).decode("utf-8")
            response = { 'success':True, 'accessToken': token } 
            return jsonify(response)
        except Exception as e:
            print('generate exception ',e)
            response = { 'success':False, 'accessToken': 'error_generating_token' + str(e).replace(' ','_') }
            return jsonify(response)

# Appointment Confirmation endpoint
class AppointmentConfirmation(Resource):
    def __init__(self):
        self._twilio_service = TwilioService()

    def get(self):
        try:
            # retrieving args from the query url string from the request object
            args = request.args 
            # validate the args, make sure all required params are passed in from the request args
            if 'key' not in args or 'number' not in args or 'message' not in args:
                response = { 'success':'false', 'message':'Missing params key, number, or message' }
                return jsonify(response)

            # call the send_comfirmation_text_msg_to_reciever function and pass in the args
            message_sid = self._twilio_service.send_comfirmation_text_msg_to_reciever(args['key'],args['number'],args['message'])
            response = { 'success': True, 'message':'successfully confirmed {}'.format(message_sid) }
            return jsonify(response)
        
        except Exception as e: # handling error
            response = { 'success': False, 'message':'unsuccessful comfirmed - {}'.format(e) }
            return jsonify(response)

# Revieces appointment information from the webapp and sends appointment to admin's phone
class AppointmentInfo(Resource):
    def __init__(self):
        self._twilio_service = TwilioService()
    
    def post(self):
        try:
            json_data = request.get_json()
            print(json_data)
            message_info = self._twilio_service.send_appointment_info_to_admin(json_data['message'])
            response = { 'success': True, 'message': 'Sucessfully sent to admin - {}'.format(message_info) }
            return jsonify(response)
        except Exception as e:
            response = { 'success': False, 'message':'unsuccessful send to admin - {}'.format(e) }
            return jsonify(response)



api.add_resource(Main,'/')
api.add_resource(GenerateToken,'/getToken')
api.add_resource(AppointmentConfirmation, '/sendConfirmation')
api.add_resource(AppointmentInfo, '/sendAppointmentInfo')

