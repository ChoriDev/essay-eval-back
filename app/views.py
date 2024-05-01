from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.serializers import EssaySerializer
from hanspell import spell_checker

# 에세이 평가 관련 API
class Evaluator(APIView):
    # POST 요청 테스트
    def post(self, request):

        # 클라이언트가 보낸 데이터
        # QueryDict(request.data)은 immutable여서 딕셔너리로 copy
        data = request.data.copy()
        # 클라이언트에서 보낸 에세이
        essay = data.get('content')

        # TODO py-hanspell 관련 코드 작성
        spelled_text = spell_checker.check(essay).as_dict
        print(spelled_text)

        # TODO 예시로 클라이언트에 문자열 hello 리턴
        data['feedback'] = 'hello'

        serializer = EssaySerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)