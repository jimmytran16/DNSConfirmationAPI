import jwt
from uuid import uuid4
import os
import datetime

#development imports
from dotenv import load_dotenv
load_dotenv()

# Get Hashing Algorithm, and Signuture from the enviroment variables
HASHING_ALG = os.getenv('HASH_ALG')
SIGNATURE = os.getenv('SIGNATURE')

# generate a random token
def generate_random_token():
    return uuid4().hex

# generaete a Json Web Token 
def generate_JWT():
    EXPIRATION_TIME_MINUTES = 1
    EXPIRATION_TIMESTAMP = datetime.datetime.utcnow() + datetime.timedelta(minutes=EXPIRATION_TIME_MINUTES)
    RANDOM_TOKEN =  generate_random_token()
    
    token = jwt.encode({"random": RANDOM_TOKEN , "exp": EXPIRATION_TIMESTAMP}, SIGNATURE , algorithm=HASHING_ALG)
    return token

# authenticate Json Web Token
def authenticate_JWT(token,signature):
    try: 
        jwt.decode(token, signature , algorithms=[HASHING_ALG]) 
    except Exception as e:
        raise Exception(str(e))
