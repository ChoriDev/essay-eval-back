from django.http import HttpResponse
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
        essay = data.get('original_text')

        # py-hanspell 관련 코드
        total_length = len(essay)
        paragraph = []
        # TODO 하나의 단어가 나뉠 수 있음, 해결 방법 모색
        if total_length > 0 and total_length <= 500:
            paragraph.append(essay)
        elif total_length > 500 and total_length <= 1000:
            split_length = 500
            paragraph.extend([essay[i:i + split_length] for i in range(0, total_length , split_length)])
        else:
            return HttpResponse(status=400)
        
        # 잘못된 맞춤법과 띄어쓰기 단어 리스트
        wrong_spelling = []
        wrong_spacing = []
        corrected_text = ''

        for text in paragraph:
            spelled_text = spell_checker.check(text)
            corrected_text += spelled_text.checked + ' '
            words = spelled_text.words
            # TODO 리스트에 중복된 내용이 포함될 수 있음
            for key, value in words.items():
                if value == 1:
                    wrong_spelling.append(key)
                elif value == 2:
                    wrong_spacing.append(key)
        
        print(corrected_text)
        print(wrong_spelling)
        print(wrong_spacing)

        data['corrected_text'] = corrected_text
        data['wrong_spelling'] = wrong_spelling
        data['wrong_spacing'] = wrong_spacing

        serializer = EssaySerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)