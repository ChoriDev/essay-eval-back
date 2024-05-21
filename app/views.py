from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.serializers import EssaySerializer
from hanspell import spell_checker
from app.splitter import text_splitter

# 에세이 평가 관련 API
class Evaluator(APIView):
    def post(self, request):
        # 클라이언트가 보낸 데이터
        data = request.data.copy()
        essay = data.get('original_text')

        if not essay:
            return Response({'error': '에세이가 전송되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # py-hanspell 관련 코드
        total_length = len(essay)
        if total_length == 0:
            return Response({'error': '에세이를 작성해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if total_length > 1000:
            return Response({'error': '1000자 이내로 작성해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 텍스트 분할
        # TODO 에러 발생 가능성 있음, 길이 제한을 500자보다 여유롭게 설정
        paragraph = text_splitter(essay, max_len=400)

        # 잘못된 맞춤법과 띄어쓰기 단어 리스트
        wrong_spelling = []
        wrong_spacing = []
        corrected_text = ''

        for text in paragraph:
            spelled_text = spell_checker.check(text)
            corrected_text += spelled_text.checked + ' '
            words = spelled_text.words
            for key, value in words.items():
                if value == 1:
                    wrong_spelling.append(key)
                elif value == 2:
                    wrong_spacing.append(key)

        # 딕셔너리로 변환하여 중복 제거
        wrong_spelling_dict = dict.fromkeys(wrong_spelling)
        wrong_spacing_dict = dict.fromkeys(wrong_spacing)

        data['corrected_text'] = corrected_text.strip()
        data['wrong_spelling'] = list(wrong_spelling_dict)
        data['wrong_spacing'] = list(wrong_spacing_dict)

        serializer = EssaySerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)