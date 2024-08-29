import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from rest_framework.exceptions import AuthenticationFailed

SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key') 
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')

def get_token(user_id):
    payload = {
        "user_id": str(user_id),  # Convert UUID to string if necessary
        "exp": datetime.utcnow() + timedelta(minutes=60),  # Token expiration time
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def decode_token_user_id(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token["user_id"] 
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except JWTError:
        raise AuthenticationFailed("Invalid token")
