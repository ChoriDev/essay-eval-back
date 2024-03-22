from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.serializers import FeedbackSerializer

# 에세이 평가 관련 API
class Evaluator(APIView):
    # POST 요청 테스트
    def post(self, request):

        # 클라이언트에서 보낸 에세이
        essay = request.data.get('essayContent')

        # 클라이언트에게 보낼 피드백
        feedback = {"feedbackContent": "good"}

        serializer = FeedbackSerializer(data=feedback)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)