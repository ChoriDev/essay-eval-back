from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.models import Essay
from app.serializers import EssaySerializer

# 에세이 평가 관련 API
class Evaluator(APIView):
    # POST 요청 테스트
    def post(self, request):
        print(request.data)
        serializer = EssaySerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)