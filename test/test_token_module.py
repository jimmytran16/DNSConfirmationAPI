import unittest
import os
from dotenv import load_dotenv
load_dotenv()

from api.token.tokenizer import *

class TestToken(unittest.TestCase):
    def setUp(self):
        self.SIGNATURE = os.getenv('SIGNATURE')
        self.apiKey = os.getenv('API_KEY')
        self.INVALID_TOKENS = [
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.fwpMeJf36POk6yJV_adQssw5cSflKxwRJSMeKKF2QT4',
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImp0aSI6IjUxMDU0NjcxLTkzODItNDRiZi1hNGI3LWM0YWZjYTc3YWMzMSIsImlhdCI6MTYxODI4MTA1NiwiZXhwIjoxNjE4Mjg0NjU2fQ.NFwxUFJ58fDt0C7CRywfI7qCc_O2rFrylit151bD_Z0',
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNjE4MjgxMDU2LCJleHAiOjE2MTgyODQ2OTUsImp0aSI6IjJkMGVkNjRkLWRlODQtNDg4NC1iNDYzLWI4MTFiNzgyYTViNiJ9.4-VT3VO8dLnTpgn-6uqllCXaH-R7Nqdy-vzWFqhllRM',
        ]
        self.expiredToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyYW5kb20iOiI1Njk3OGRkZDU5NmY0M2M0OWU3NmYwNzkxNDg0YWJlNSIsImV4cCI6MTYxOTY2MTM0MX0.AxZL6y88wGZ2zXBks4wAnd689Q_lPAubsL6a40gS2aw'

    # Test to see that the generate_JWT() function should return back a byte datatype of the token  
    def test_generate_jwt_func(self):
        self.assertEqual(type(generate_JWT(self.apiKey)), type(bytes()))
    
    # Test the authenticate_JWT() function by passing in a valid token, should return true
    def test_authenticate_jwt_func(self):
        token = generate_JWT(self.apiKey)
        result = authenticate_JWT(token, self.SIGNATURE)
        self.assertEqual(result,None)


    # Will test a list of invalid tokens on the authenicate_JWT function.
    # All function calls should give expcetion and return message "Signature verification failed"
    def test_authenticate_with_invalid_tokens_0(self):
        try:
            authenticate_JWT(self.INVALID_TOKENS[0], self.SIGNATURE)
        except Exception as e:
            self.assertEqual(str(e),'Signature verification failed')
    
    def test_authenticate_with_invalid_tokens_1(self):
        try:
            authenticate_JWT(self.INVALID_TOKENS[1], self.SIGNATURE)
        except Exception as e:
            self.assertEqual(str(e),'Signature verification failed')
    
    def test_authenticate_with_invalid_tokens_2(self):
        try:
            authenticate_JWT(self.INVALID_TOKENS[2], self.SIGNATURE)
        except Exception as e:
            self.assertEqual(str(e),'Signature verification failed')
    
    def test_authenticate_with_invalid_tokens_3(self):
        try:
            authenticate_JWT(self.INVALID_TOKENS[3], self.SIGNATURE)
        except Exception as e:
            self.assertEqual(str(e),'Signature verification failed')
    
    def test_authenticate_with_expired_token(self):
        try:
            authenticate_JWT(self.expiredToken, self.SIGNATURE)
        except Exception as e:
            self.assertEqual(str(e),'Signature has expired')
            
    
