import os
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# 환경 변수 설정
target_model = "klue/bert-base"
num_labels = 1
base_dir = os.path.dirname(__file__)
model_file = os.path.join(base_dir, "models/exp3_model.pth")

# 모델과 토크나이저를 전역 변수로 로드
BERT_MODEL = BertForSequenceClassification.from_pretrained(target_model, num_labels=num_labels)
BERT_TOKENIZER = BertTokenizer.from_pretrained(target_model)

# GPU가 없는 경우 모델을 CPU로 매핑하여 로드
BERT_MODEL.load_state_dict(torch.load(model_file, map_location=torch.device('cpu')))
BERT_MODEL.eval()

def predict(chunks):
    """ 텍스트 입력을 받아 BERT 모델을 사용하여 점수를 예측하고 평균 점수를 반환 """
    # text_splitter를 사용하여 텍스트를 512 토큰 이하로 나눔
    max_len = 512  # BERT는 512이므로 내부 변수로 고정

    # 각 문단에 대한 점수를 계산
    scores = []
    for chunk in chunks:
        inputs = BERT_TOKENIZER(chunk, return_tensors="pt", padding='max_length', max_length=max_len, truncation=True)
        inputs = {key: value for key, value in inputs.items()}
        with torch.no_grad():
            outputs = BERT_MODEL(**inputs)
            prediction = outputs.logits.squeeze().item()
            scores.append(prediction)

    # 평균 점수 계산
    if scores:
        average_score = sum(scores) / len(scores)
    else:
        average_score = None  # 문단이 없는 경우 None 반환

    return average_score

# 테스트
# multiplier = 15
# text = ("이 문장은 예제로 만들어졌습니다. BERT 모델을 사용하여 텍스트를 처리하고 있습니다. "
#         "이 프로젝트는 자연어 처리 기술을 활용하여 텍스트의 의미를 분석하고, 해당 텍스트의 점수를 예측하는 것이 목표입니다. ") * multiplier
# print(len(text))
# score = predict(text)
# print("Score:", score)

def feedback(chunks):
    score = round(predict(chunks), 2)
    comment = ''

    if score >= 2.5:
        comment = '매우 우수'
    elif score >= 2.0:
        comment = '우수'
    elif score >= 1.5:
        comment = '보통'
    elif score >= 1.0:
        comment = '미흡'
    else:
        comment = '매우 미흡'
    
    return {'score': score, 'comment': comment}