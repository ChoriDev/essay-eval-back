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
        print('essay: ', essay)

        # TODO py-hanspell 관련 코드 작성

        if len(essay) > 500:
            return Response({'error': '글자수 초과'}, status=status.HTTP_400_BAD_REQUEST)

        spelled_text = spell_checker.check(essay)

        original_essay = spelled_text.original
        corrected_essay = spelled_text.checked
        num_error = spelled_text.errors
        words = spelled_text.words

        corrected_spelling = []
        corrected_spacing = []

        # for key, value in words.items():
        #     if value == 1:
        #         corrected_spelling.append(key)
        #     elif value == 2:
        #         corrected_spacing.append(key)
        corrected_spelling = [key for key, value in words.items() if value == 1]
        corrected_spacing = [key for key, value in words.items() if value == 2]


        # data['corrected_essay'] = corrected_essay
        # data['corrected_spelling'] = corrected_spelling
        # data['corrected_spacing'] = corrected_spacing
        feedback = {
        "corrected_spelling": corrected_spelling,
        "corrected_spacing": corrected_spacing
        }

        data['corrected_essay'] = corrected_essay
        data['feedback'] = feedback

        # ==========================================
        

        # TODO 예시로 클라이언트에 문자열 hello 리턴
        # data['feedback'] = 'hello'

        serializer = EssaySerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)