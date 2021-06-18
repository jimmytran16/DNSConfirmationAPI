import unittest, json, os
from api import app
from dotenv import load_dotenv
load_dotenv()

from api.services.token.token_service import TokenizerService

class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.SIGNATURE = os.getenv('SIGNATURE')
        self.apiKey = os.getenv('API_KEY')
        self.client = app.test_client()
        self.headerConfig = { "Content-Type": "application/json" }
        self.getTokenEndpoint = '/getToken'
        self.sendConfirmationEndpoint = '/sendConfirmation'
        self.testPhoneNumber = os.getenv('TEST_RECIEVER')
        self.INVALID_TOKENS = [
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.fwpMeJf36POk6yJV_adQssw5cSflKxwRJSMeKKF2QT4',
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImp0aSI6IjUxMDU0NjcxLTkzODItNDRiZi1hNGI3LWM0YWZjYTc3YWMzMSIsImlhdCI6MTYxODI4MTA1NiwiZXhwIjoxNjE4Mjg0NjU2fQ.NFwxUFJ58fDt0C7CRywfI7qCc_O2rFrylit151bD_Z0',
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNjE4MjgxMDU2LCJleHAiOjE2MTgyODQ2OTUsImp0aSI6IjJkMGVkNjRkLWRlODQtNDg4NC1iNDYzLWI4MTFiNzgyYTViNiJ9.4-VT3VO8dLnTpgn-6uqllCXaH-R7Nqdy-vzWFqhllRM',
        ]
        self.NOT_ENOUGH_SEGMENT_TOKENS = [
            '123',
            'ejfowejfoiewjfioejwfiowejfoiwejiofjweoiew',
            'CIBgbQbNqtJPJNQpD6AE94tkagFM6j0h',
            '!'
        ]
        self._tokenizer_serivce = TokenizerService()

    def tearDown(self):
        pass

# +---------------------------------+
# | HELPER functions                |
# +---------------------------------+

    # function to get response 
    def get_response(self,url):
        return self.client.get(url, headers=self.headerConfig)

    def parse_response_data(self,response):
        return json.loads(response.decode('utf-8'))


# +---------------------------------+
# | TESTING /getToken endpoint      | 
# +---------------------------------+
# All cases are asserting the response data, response status code, and response headers

    # test a success request call for endpoint passing in correct parameters
    def test_successful_generate_token_endpoint(self):
        url = self.getTokenEndpoint + '?apiKey={}'.format(self.apiKey)
        response = self.get_response(url)
        response_data = self.parse_response_data(response.data)
        
        self.assertEqual(2,len(response_data))   
        self.assertEqual(200, response.status_code)
        self.assertEqual(True,response_data['success'])
        self.assertEqual('application/json',response.headers[0][1])

    # test a unsucessful request call for endpoint passing in an invalid API key
    def test_unsuccessful_generate_token_endpoint_wrong_api_key(self):
        invalid_api_key = '123321123321'
        url = self.getTokenEndpoint + '?apiKey={}'.format(invalid_api_key)
        response = self.get_response(url)
        response_data = self.parse_response_data(response.data)

        self.assertEqual(False,response_data['success'])
        self.assertEqual('error_generating_tokenInvalid_API_KEY',response_data['accessToken'])
        self.assertEqual(200,response.status_code)
        self.assertEqual('application/json',response.headers[0][1])

    # test a unsuccessful request call for endpoint not passing in a required API key parameter
    def test_unsuccessful_generate_token_endpoint_no_api_key(self):
        url = self.getTokenEndpoint
        response = self.get_response(url)
        response_data = self.parse_response_data(response.data)

        self.assertEqual(200,response.status_code)
        self.assertEqual('error_generating_token400_Bad_Request:_The_browser_(or_proxy)_sent_a_request_that_this_server_could_not_understand.'
                                    ,response_data['accessToken'])
        self.assertFalse(response_data['success'])
        self.assertEqual('application/json',response.headers[0][1])


# +------------------------------------+
# | TESTING /sendConfirmation endpoint |
# +------------------------------------+

    # test a successful request to the endpoint
    def test_successful_send_confirmation_endpoint(self):
       
        jwt = self._tokenizer_serivce.generate_JWT(self.apiKey).decode('utf-8')
        query_parameters = '?key={}&number={}&message=hi%20this%20is%20for%20testing%20message.%20'.format(jwt,self.testPhoneNumber)
        url = self.sendConfirmationEndpoint + query_parameters
        response = self.get_response(url)
        response_data = self.parse_response_data(response.data)
        
        self.assertEqual(True,response_data['success'])
        self.assertEqual(200,response.status_code)
        self.assertEqual('application/json',response.headers[0][1])
        self.assertIn("successfully confirmed",response_data['message'])

    # test an unsuccessful request to the endpoint, passing in an invalid JWT
    def test_unsuccessful_send_confirmation_endpoint_wrong_jwt_token(self):
           
        invalid_tokens = self.INVALID_TOKENS
        query_parameter_string = '?key={}&number={}&message=hi%20this%20is%20for%20testing%20message.%20'
        # loop through the invalid tokens and call the /sendConfirmation endpoint
        # asserts success is false, response status is 200, response message
        for token in invalid_tokens:
            query_parameters = query_parameter_string.format(token,self.testPhoneNumber)
            url = self.sendConfirmationEndpoint + query_parameters
            response = self.get_response(url)
            response_data = self.parse_response_data(response.data)
            
            self.assertFalse(response_data['success'])
            self.assertIn("Signature verification failed",response_data['message'])
            self.assertEqual('application/json',response.headers[0][1])
            self.assertEqual(200,response.status_code)

    # test an unsuccessful request to endpoint, passing in JWT tokens that are not of required length
    def test_unsuccessful_send_confirmation_endpoint_not_enough_segments(self):

        not_enough_segment_tokens = self.NOT_ENOUGH_SEGMENT_TOKENS
        query_parameter_string = '?key={}&number={}&message=hi%20this%20is%20for%20testing%20message.%20'
        # loop through the tokens that don't have enough segments and call the /sendConfirmation endpoint
        # asserts success is false, response status is 200, response message
        for token in not_enough_segment_tokens:
            query_parameters = query_parameter_string.format(token,self.testPhoneNumber)
            url = self.sendConfirmationEndpoint + query_parameters
            response = self.get_response(url)
            response_data = self.parse_response_data(response.data)

            self.assertFalse(response_data['success'])
            self.assertIn("Not enough segments",response_data['message'])
            self.assertEqual('application/json',response.headers[0][1])
            self.assertEqual(200,response.status_code)



        

    




