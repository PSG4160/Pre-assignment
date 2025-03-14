from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed as JWTAuthFailed
from rest_framework.response import Response
from rest_framework import status
from .errors import ERRORS

def error_response(error_key, status_code):
    return Response({"error": ERRORS[error_key]}, status=status_code)

def custom_jwt_exception_handler(exc, context):
    if isinstance(exc, InvalidToken):
        return error_response("INVALID_TOKEN", status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, TokenError):
        return error_response("TOKEN_EXPIRED", status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, JWTAuthFailed) or isinstance(exc, AuthenticationFailed):
        return error_response("TOKEN_NOT_FOUND", status.HTTP_401_UNAUTHORIZED)

    return None