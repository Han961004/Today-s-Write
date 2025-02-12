from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ..models.user import User


## 로그아웃을 다룰 뷰 (미완)
class LogoutView(APIView):
    '''
    로그아웃을 처리하는 View
    인증된 사용자의 토큰을 삭제합니다.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Authorization 헤더에서 토큰 값 추출
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Token "):
            return Response({"detail": "Invalid token format."}, status=status.HTTP_400_BAD_REQUEST)

        # 'Token <key>' 형식에서 실제 키 추출
        token_key = auth_header.split(" ")[1]

        # 토큰 검색 및 삭제
        token = get_object_or_404(Token, key=token_key)
        token.delete()

        return Response({"message": "Logged out successfully."}, status=status.HTTP_204_NO_CONTENT)