import jwt
import datetime
import os
from fastapi import status
import functools
from fastapi.responses import JSONResponse


JWT_SECRET = os.environ["JWT_SECRET"]


def create_jwt(payload, expiration_minutes=60*24):
    """
    Create a JSON Web Token (JWT).

    :param payload: A dictionary containing the data you want to include in the JWT.
    :param expiration_minutes: The number of minutes until the token expires (default: 30 minutes).
    :return: The JWT as a string.
    """
    # Calculate the expiration time
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)

    # Add the expiration time to the payload
    payload['exp'] = expiration_time

    # Create the JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

    return token


def validate_jwt(token):
    """
    Validate a JSON Web Token (JWT).

    :param token: The JWT to be validated.
    :return: The payload of the JWT if valid, or None if invalid.
    """
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

        # Check if the token has expired
        current_time = datetime.datetime.utcnow()
        if 'exp' in payload and current_time < datetime.datetime.utcfromtimestamp(payload['exp']):
            return {"valid":True, "payload":payload}
        else:
            return {"valid":False, "message":"Token Invalid"}
    except jwt.ExpiredSignatureError:
        return {"valid":False, "message":"Token has expired"}
    except Exception:
        return {"valid":False, "message":"Token Invalid"}



def auth_required(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        token = request.cookies.get("token","")
        result = validate_jwt(token)
        if  result["valid"]:
            kwargs["token"] = result["payload"]["id"]
            result = await func(*args, **kwargs)
            return result
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content={"message":result.get("message","Token Invalid")})
    return wrapper
    