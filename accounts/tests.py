import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

@pytest.mark.django_db
def test_signup_success():
    """회원가입 성공 테스트"""
    client = APIClient()
    response = client.post("/signup/", {
        "username": "testuser",
        "password": "password123",
        "nickname": "tester"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "testuser"

@pytest.mark.django_db
def test_signup_fail_user_exists():
    """이미 가입된 사용자 회원가입 실패 테스트"""
    User.objects.create_user(username="testuser", password="password123", nickname="tester")
    client = APIClient()
    response = client.post("/signup/", {
        "username": "testuser",
        "password": "password123",
        "nickname": "tester"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"]["code"] == "USER_ALREADY_EXISTS"

@pytest.mark.django_db
def test_login_success():
    """로그인 성공 테스트"""
    User.objects.create_user(username="testuser", password="password123", nickname="tester")
    client = APIClient()
    response = client.post("/login/", {
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()

@pytest.mark.django_db
def test_login_fail_invalid_credentials():
    """로그인 실패 테스트 - 잘못된 비밀번호"""
    User.objects.create_user(username="testuser", password="password123", nickname="tester")
    client = APIClient()
    response = client.post("/login/", {
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"
