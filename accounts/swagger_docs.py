from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterSerializer, UserSerializer

# 회원가입 API 문서화
register_schema = swagger_auto_schema(
    operation_summary="회원가입 API",
    operation_description="새로운 사용자를 등록합니다.",
    request_body=RegisterSerializer,
    responses={
        201: openapi.Response(
            description="회원가입 성공",
            schema=UserSerializer
        ),
        400: openapi.Response(
            description="이미 가입된 사용자입니다.",
            examples={
                "application/json": {
                    "error": {
                        "code": "USER_ALREADY_EXISTS",
                        "message": "이미 가입된 사용자입니다."
                    }
                }
            }
        )
    }
)

# 로그인 API 문서화
login_schema = swagger_auto_schema(
    operation_summary="로그인 API",
    operation_description="사용자 로그인 후 JWT 토큰을 반환합니다.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "password"],
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="사용자 이름"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호"),
        },
    ),
    responses={
        200: openapi.Response(
            description="로그인 성공",
            examples={
                "application/json": {
                    "token": "JWT_ACCESS_TOKEN"
                }
            }
        ),
        400: openapi.Response(
            description="로그인 실패",
            examples={
                "application/json": {
                    "error": {
                        "code": "INVALID_CREDENTIALS",
                        "message": "아이디 또는 비밀번호가 올바르지 않습니다."
                    }
                }
            }
        ),
    }
)

# 보호된 API 문서화 (JWT 인증 필요)
protected_schema = swagger_auto_schema(
    operation_summary="보호된 API (JWT 인증 필요)",
    operation_description="""
이 API는 JWT 인증이 필요합니다.  
Authorization 헤더에 Bearer 토큰을 포함해야 합니다.

#### ❌ **인증 실패 예제**
```json
{
  "error": {
    "code": "TOKEN_NOT_FOUND",
    "message": "토큰이 없습니다."
  }
}

{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "토큰이 유효하지 않습니다."
  }
}

{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "토큰이 만료되었습니다."
  }
}
```""",
    manual_parameters=[
        openapi.Parameter(
            name="Authorization",
            in_=openapi.IN_HEADER,
            description="Bearer 액세스 토큰 (JWT)",
            type=openapi.TYPE_STRING,
            required=True,
            example="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        )
    ],
    responses={
        200: openapi.Response(
            description="인증 성공",
            examples={
                "application/json": {
                    "message": "이 API는 인증된 사용자만 접근할 수 있습니다."
                }
            }
        ),
        401: openapi.Response(
            description="인증 실패",
            examples={
                "TOKEN_NOT_FOUND": {
                    "application/json": {
                        "error": {
                            "code": "TOKEN_NOT_FOUND",
                            "message": "토큰이 없습니다."
                        }
                    }
                },
                "INVALID_TOKEN": {
                    "application/json": {
                        "error": {
                            "code": "INVALID_TOKEN",
                            "message": "토큰이 유효하지 않습니다."
                        }
                    }
                },
                "TOKEN_EXPIRED": {
                    "application/json": {
                        "error": {
                            "code": "TOKEN_EXPIRED",
                            "message": "토큰이 만료되었습니다."
                        }
                    }
                }
            }
        )
    }
)