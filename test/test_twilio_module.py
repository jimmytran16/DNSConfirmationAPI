import unittest
from api.twilio.send import send_comfirmation_text_msg_to_reciever
from api.token.tokenizer import generate_JWT

import os
from dotenv import load_dotenv
load_dotenv()

# Test case for testing the Twilio module
class TestTwilioModule(unittest.TestCase):
    # set up initializations variables that will be used in test case functions
    def setUp(self):
        self.invalidKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        self.expiredToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyYW5kb20iOiI1Njk3OGRkZDU5NmY0M2M0OWU3NmYwNzkxNDg0YWJlNSIsImV4cCI6MTYxOTY2MTM0MX0.AxZL6y88wGZ2zXBks4wAnd689Q_lPAubsL6a40gS2aw'
        self.body = "This is Designer Nail Salon confirming your appointment for 01/20/2021 at 6:00PM -- TESTING"
        self.apiKey = os.getenv('API_KEY')
        self.reciever = os.getenv('TEST_RECIEVER')
    
    # Test the send confirmation function - passing in a invalid token
    # There should be an Exception with the message saying 'Signature verification failed'
    def test_send_comfirmation_func_with_invalid_token(self):
        try:
            data = send_comfirmation_text_msg_to_reciever(self.invalidKey,self.reciever,self.body)
            self.assertEqual(data['to'], self.reciever)
            self.assertEqual(data['body'],self.body)
        except Exception as e:
            self.assertEqual(str(e),'Signature verification failed')
    
    # Test the send confirmation function - passing in a expired token
    # There should be an Exception with the message saying 'Signature has expired'
    def test_send_comfirmation_func_with_expired_token(self):
        try:
            send_comfirmation_text_msg_to_reciever(self.expiredToken,self.reciever,self.body)
        except Exception as e:
            self.assertEqual(str(e),'Signature has expired')
    
    # Test the send confirmation function - passing in a valid token
    # Should be able to call function without any exceptions
    def test_send_comfirmation_func_with_valid_token(self):
        validToken = generate_JWT(self.apiKey)
        result = send_comfirmation_text_msg_to_reciever(validToken,self.reciever,self.body)
        self.assertEqual(result['to'], '+1{}'.format(self.reciever))
        self.assertEqual(result['body'],self.body)        
        self.assertEqual(result['from'],'+1{}'.format(os.getenv('SENDER_NUMBER')))
        self.assertEqual(len(result),4)
