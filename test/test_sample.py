import unittest
import os
from dotenv import load_dotenv
load_dotenv()

from api.token.tokenizer import *

class TestToken(unittest.TestCase):
    def setUp(self):
        self.SIGNATURE = os.getenv('SIGNATURE')
        self.INVALID_TOKENS = [
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.fwpMeJf36POk6yJV_adQssw5cSflKxwRJSMeKKF2QT4',
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImp0aSI6IjUxMDU0NjcxLTkzODItNDRiZi1hNGI3LWM0YWZjYTc3YWMzMSIsImlhdCI6MTYxODI4MTA1NiwiZXhwIjoxNjE4Mjg0NjU2fQ.NFwxUFJ58fDt0C7CRywfI7qCc_O2rFrylit151bD_Z0',
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNjE4MjgxMDU2LCJleHAiOjE2MTgyODQ2OTUsImp0aSI6IjJkMGVkNjRkLWRlODQtNDg4NC1iNDYzLWI4MTFiNzgyYTViNiJ9.4-VT3VO8dLnTpgn-6uqllCXaH-R7Nqdy-vzWFqhllRM',
        ]

    # Test to see that the generate_JWT() function should return back a byte datatype of the token  
    def test_generate_jwt_func(self):
        self.assertEqual(type(generate_JWT()), type(bytes()))
    
    # Test the authenticate_JWT() function by passing in a valid token, should return true
    def test_authenticate_jwt_func(self):
        token = generate_JWT()
        self.assertEqual(authenticate_JWT(token,self.SIGNATURE), True)

    # Will test a list of invalid tokens on the authenicate_JWT function.
    # Function should return all false values
    def test_authenticate_invalid_tokens(self):
        for token in self.INVALID_TOKENS:
            self.assertEqual(authenticate_JWT(token,SIGNATURE),False)
