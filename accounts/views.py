from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
from .models import User
from .errors import ERRORS
from .swagger_docs import register_schema, login_schema, protected_schema  # Swagger 문서화 분리

def error_response(error_key, status_code):
    return Response({"error": ERRORS[error_key]}, status=status_code)

def success_response(data, status_code=status.HTTP_200_OK):
    return Response(data, status=status_code)

def generate_tokens(user):
    """JWT 액세스 토큰 생성"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

# 회원가입 API
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @register_schema  # Swagger 문서 적용
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return success_response(UserSerializer(user).data, status.HTTP_201_CREATED)

        return error_response("USER_ALREADY_EXISTS", status.HTTP_400_BAD_REQUEST)

# 로그인 API
class LoginView(APIView):
    permission_classes = [AllowAny]

    @login_schema  # Swagger 문서 적용
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            return success_response({"token": generate_tokens(user)})

        return error_response("INVALID_CREDENTIALS", status.HTTP_400_BAD_REQUEST)

# 토큰 확인용 API (인증 필요)
class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @protected_schema
    def get(self, request):
        return Response({"message": "이 API는 인증된 사용자만 접근할 수 있습니다."})
