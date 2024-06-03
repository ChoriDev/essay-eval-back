import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from app.serializers import EssaySerializer
from hanspell import spell_checker
from app.splitter import split_by_up_to_400_characters, split_by_512_tokens
from evaluator import BertEvaluator

# 모델 파일 경로 설정
base_dir = os.path.dirname(__file__)
model_files = {
    "cont1": os.path.join(base_dir, "models/cont1_model.pth"),
    "cont2": os.path.join(base_dir, "models/cont2_model.pth"),
    "exp2": os.path.join(base_dir, "models/exp2_model.pth"),
    "exp3": os.path.join(base_dir, "models/exp3_model.pth"),
    "org3": os.path.join(base_dir, "models/org3_model.pth")
}

# 에세이 평가 관련 API
class Evaluator(APIView):
    def post(self, request):
        # 클라이언트가 보낸 데이터
        data = request.data.copy()
        essay_content = data.get('original_text')

        if not essay_content:
            return Response({'error': '에세이가 전송되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        essay_length = len(essay_content)
        if essay_length == 0:
            return Response({'error': '에세이를 작성해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if essay_length > 1000:
            return Response({'error': '1000자 이내로 작성해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 텍스트 분할
        splitted_by_400_characters_chunks = split_by_up_to_400_characters(essay_content)
        splitted_by_512_tokens_chunks = split_by_512_tokens(essay_content)

        # py-hanspell 관련 코드
        wrong_spelling = []
        wrong_spacing = []
        corrected_text = ''

        for text in splitted_by_400_characters_chunks:
            spelled_text = spell_checker.check(text)
            corrected_text += spelled_text.checked + ' '
            words = spelled_text.words
            for key, value in words.items():
                if value == 1:
                    wrong_spelling.append(key)
                elif value == 2:
                    wrong_spacing.append(key)

        wrong_spelling_dict = dict.fromkeys(wrong_spelling)
        wrong_spacing_dict = dict.fromkeys(wrong_spacing)

        # 각 모델의 피드백을 저장할 딕셔너리
        feedback_results = {}

        # 모델 평가
        for model_name, model_path in model_files.items():
            evaluator = BertEvaluator(model_path)
            feedback_results[model_name] = evaluator.feedback(splitted_by_512_tokens_chunks)

        # 결과 데이터에 추가
        data['corrected_text'] = corrected_text.strip()
        data['wrong_spelling'] = list(wrong_spelling_dict)
        data['wrong_spacing'] = list(wrong_spacing_dict)
        data['cont1_score'] = feedback_results['cont1']['score']
        data['cont1_comment'] = feedback_results['cont1']['comment']
        data['cont2_score'] = feedback_results['cont2']['score']
        data['cont2_comment'] = feedback_results['cont2']['comment']
        data['exp2_score'] = feedback_results['exp2']['score']
        data['exp2_comment'] = feedback_results['exp2']['comment']
        data['exp3_score'] = feedback_results['exp3']['score']
        data['exp3_comment'] = feedback_results['exp3']['comment']
        data['org3_score'] = feedback_results['org3']['score']
        data['org3_comment'] = feedback_results['org3']['comment']

        serializer = EssaySerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)