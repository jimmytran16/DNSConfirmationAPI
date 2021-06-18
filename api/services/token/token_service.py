import jwt
from uuid import uuid4
import os
import datetime

#development imports
from dotenv import load_dotenv
load_dotenv()

class TokenizerService:
    def __init__(self):
        # Get Hashing Algorithm, and Signuture from the enviroment variables, and expiration time in hours
        self.HASHING_ALG = os.getenv('HASH_ALG')
        self.SIGNATURE = os.getenv('SIGNATURE')
        self.EXPIRATION_TIME_HOURS = int(os.getenv('EXPIRATION_TIME'))
        self.API_KEY=os.getenv('API_KEY')

    # generate a random token
    def generate_random_token(self):
        return uuid4().hex

    # generate a Json Web Token 
    def generate_JWT(self,apiKey):
        if (apiKey != self.API_KEY):
            raise Exception('Invalid_API_KEY')
        else:
            EXPIRATION_TIMESTAMP = datetime.datetime.utcnow() + datetime.timedelta(hours=self.EXPIRATION_TIME_HOURS)
            RANDOM_TOKEN =  self.generate_random_token()
            token = jwt.encode({"random": RANDOM_TOKEN , "exp": EXPIRATION_TIMESTAMP}, self.SIGNATURE , algorithm=self.HASHING_ALG)
            return token

    # authenticate Json Web Token
    def authenticate_JWT(self,token,signature):
        try: 
            jwt.decode(token, signature , algorithms=[self.HASHING_ALG]) 
        except Exception as e:
            raise Exception(str(e))


# if __name__ == '__main__':
    # print(authenticate_JWT('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyYW5kb20iOiI1Njk3OGRkZDU5NmY0M2M0OWU3NmYwNzkxNDg0YWJlNSIsImV4cCI6MTYxOTY2MTM0MX0.AxZL6y88wGZ2zXBks4wAnd689Q_lPAubsL6a40gS2aw',SIGNATURE))
