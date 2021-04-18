import unittest, json, os
from api import app
from dotenv import load_dotenv
load_dotenv()

from api.token.tokenizer import generate_JWT

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

    def test_successful_generate_token_endpoint(self):
        url = self.getTokenEndpoint + '?apiKey={}'.format(self.apiKey)
        response = self.get_response(url)
        response_data = self.parse_response_data(response.data)
        
        self.assertEqual(2,len(response_data))   
        self.assertEqual(200, response.status_code)
        self.assertEqual(True,response_data['success'])
        self.assertEqual('application/json',response.headers[0][1])

    
    def test_unsuccessful_generate_token_endpoint_wrong_api_key(self):
        invalid_api_key = '123321123321'
        url = self.getTokenEndpoint + '?apiKey={}'.format(invalid_api_key)
        response = self.get_response(url)
        response_data = self.parse_response_data(response.data)

        self.assertEqual(False,response_data['success'])
        self.assertEqual('error_generating_tokenInvalid_API_KEY',response_data['accessToken'])
        self.assertEqual(200,response.status_code)
        self.assertEqual('application/json',response.headers[0][1])

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

    def test_successful_send_confirmation_endpoint(self):
       
        jwt = generate_JWT(self.apiKey).decode('utf-8')
        query_parameters = '?key={}&number={}&message=hi%20this%20is%20for%20testing%20message.%20'.format(jwt,self.testPhoneNumber)
        url = self.sendConfirmationEndpoint + query_parameters
        response = self.get_response(url)
        response_data = self.parse_response_data(response.data)
        
        print(response_data)
        self.assertEqual(True,response_data['success'])
        self.assertEqual(200,response.status_code)
        self.assertEqual('application/json',response.headers[0][1])
        self.assertIn("successfully confirmed",response_data['message'])

    def test_unsuccessful_send_confirmation_endpoint_wrong_jwt_token(self):
           
        invalid_jwt_1 = self.INVALID_TOKENS[0]
        invalid_jwt_2 = self.INVALID_TOKENS[1]
        
        query_parameters_1 = '?key={}&number={}&message=hi%20this%20is%20for%20testing%20message.%20'.format(invalid_jwt_1,self.testPhoneNumber)
        query_parameters_2 = '?key={}&number={}&message=hi%20this%20is%20for%20testing%20message.%20'.format(invalid_jwt_2,self.testPhoneNumber)
        
        url_1 = self.sendConfirmationEndpoint + query_parameters_1
        url_2 = self.sendConfirmationEndpoint + query_parameters_2

        response_1 = self.get_response(url_1)
        response_2 = self.get_response(url_2)

        response_data_1 = self.parse_response_data(response_1.data)
        response_data_2 = self.parse_response_data(response_2.data)

        
        self.assertFalse(response_data_1['success'])
        self.assertIn("Signature verification failed",response_data_1['message'])
        self.assertEqual('application/json',response_1.headers[0][1])
        
        self.assertFalse(response_data_2['success'])
        self.assertIn("Signature verification failed",response_data_2['message'])
        self.assertEqual('application/json',response_2.headers[0][1])


    




