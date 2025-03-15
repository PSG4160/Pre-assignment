from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed as JWTAuthFailed
from rest_framework.response import Response
from rest_framework import status
from .errors import ERRORS
#import logging

#logger = logging.getLogger(__name__)

def error_response(error_key, status_code):
    return Response({"error": ERRORS[error_key]}, status=status_code)

def custom_jwt_exception_handler(exc, context):
    #logger.error(f"JWT exception encountered: {exc}", exc_info=True)
    
    # TokenError 및 InvalidToken 모두 처리
    if isinstance(exc, (TokenError, InvalidToken)):
        detail = getattr(exc, 'detail', None)
        if isinstance(detail, dict):
            messages = detail.get("messages", [])
            for msg in messages:
                message_text = str(msg.get("message", "")).lower()
                if "expired" in message_text:
                    return error_response("TOKEN_EXPIRED", status.HTTP_401_UNAUTHORIZED)
        # fallback: 문자열 검사
        if "expired" in str(exc).lower():
            return error_response("TOKEN_EXPIRED", status.HTTP_401_UNAUTHORIZED)
        return error_response("INVALID_TOKEN", status.HTTP_401_UNAUTHORIZED)
    
    if isinstance(exc, NotAuthenticated):
        return error_response("TOKEN_NOT_FOUND", status.HTTP_401_UNAUTHORIZED)
    
    if isinstance(exc, (JWTAuthFailed, AuthenticationFailed)):
        return error_response("INVALID_TOKEN", status.HTTP_401_UNAUTHORIZED)
    
    return None
