import torch
from transformers import BertTokenizer, BertForSequenceClassification

class BertEvaluator:
    def __init__(self, model_name, model_path):
        target_model = "klue/bert-base"
        num_labels = 1
        self.tokenizer = BertTokenizer.from_pretrained(target_model)
        self.model = BertForSequenceClassification.from_pretrained(target_model, num_labels=num_labels)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()
        self.model_name = model_name

    def predict(self, chunks):
        max_len = 512
        scores = []

        for chunk in chunks:
            inputs = self.tokenizer(chunk, return_tensors="pt", padding='max_length', max_length=max_len, truncation=True)
            inputs = {key: value for key, value in inputs.items()}
            with torch.no_grad():
                outputs = self.model(**inputs)
                prediction = outputs.logits.squeeze().item()
                scores.append(prediction)

        if scores:
            average_score = sum(scores) / len(scores)
        else:
            average_score = None

        return average_score

    def feedback(self, chunks):
        score = round(self.predict(chunks), 2)
        comment = self.generate_comment(score)
        return {'score': score, 'comment': comment}

    def generate_comment(self, score):
        model_feedback = {
            "cont1": [
                (2.5, "매우 우수합니다. 주제가 매우 명확하고 목적이 명확하게 전달되었습니다. 독자가 쉽게 이해하고 집중할 수 있습니다."),
                (2.0, "우수합니다. 주제는 명확하게 정의되어 있으며, 대체로 일관성이 있습니다."),
                (1.5, "보통입니다. 주제는 대체로 명확하지만 일부 부분에서 명확성이 부족합니다. 좀 더 명확하게 정의할 필요가 있습니다."),
                (1.0, "미흡합니다. 주제가 다소 명확하지 않고, 일관성이 부족합니다."),
                (0.0, "매우 미흡합니다. 주제가 명확하지 않고 혼란스럽습니다. 독자가 글의 주제나 목적을 이해하기 어렵습니다."),
            ],
            "cont2": [
                (2.5, "매우 우수합니다. 논지를 뒷받침하는 근거가 구체적이고 명확합니다."),
                (2.0, "우수합니다. 적절한 근거가 제시되었습니다. 더 구체적인 사례가 있으면 좋을 것 같습니다."),
                (1.5, "보통입니다. 근거가 논지를 뒷받침하지만 명확성이나 구체성이 다소 부족합니다."),
                (1.0, "미흡합니다. 근거는 있으나 논지와의 연관성이 약하고 구체성이 부족합니다."),
                (0.0, "매우 미흡합니다. 제시된 근거가 논지에 맞지 않거나 신뢰성이 부족합니다."),
            ],
            "exp2": [
                (2.5, "매우 우수합니다. 단어 선택이 매우 적절하고 효과적입니다. 문맥에 완벽하게 맞는 어휘가 사용되었고, 독자가 쉽게 이해할 수 있습니다."),
                (2.0, "우수합니다. 단어 선택이 대체로 적절하고 문맥에 잘 맞습니다."),
                (1.5, "보통입니다. 대체로 단어 선택이 적절하지만 일부 단어가 문맥에 맞지 않거나 어색할 수 있습니다."),
                (1.0, "미흡합니다. 일부 단어 선택이 어색하거나 문맥에 맞지 않는 경우가 있습니다."),
                (0.0, "매우 미흡합니다. 단어 선택이 매우 부적절하고 독자에게 혼란을 줄 수 있습니다. 문맥에 맞지 않는 어휘가 자주 사용되었습니다."),
            ],
            "exp3": [
                (2.5, "매우 우수합니다. 문장 표현이 매우 자연스럽고 읽기 쉽습니다. 문장 구조와 표현이 매우 적절하며, 독자가 내용을 이해하는 데 전혀 지장이 없습니다."),
                (2.0, "우수합니다. 문장 표현이 자연스럽고 읽기 쉽습니다. 대체로 일관성이 있으며 전반적으로 잘 구성되었습니다."),
                (1.5, "보통입니다. 대체로 문장 표현이 적절하지만 일부 부분에서 어색하거나 혼란스러운 표현이 있습니다."),
                (1.0, "미흡합니다. 문장 표현이 다소 어색하고 일관성이 부족합니다. 좀 더 자연스럽게 표현을 바꿀 필요가 있습니다."),
                (0.0, "매우 미흡합니다. 문장 구조나 표현이 혼란스럽고 어색합니다. 독자가 이해하기 어려운 문장들이 많습니다."),
            ],
            "org3": [
                (2.5, "매우 우수합니다. 글의 구조가 매우 명확하고 일관성 있습니다. 모든 문장이 자연스럽게 연결되어 있고, 독자가 쉽게 따라갈 수 있습니다."),
                (2.0, "우수합니다. 구조가 명확하고 일관성이 있습니다. 대부분의 문장이 잘 연결되어 있으며, 전반적으로 구성이 잘 되어 있습니다."),
                (1.5, "보통입니다. 대체로 구조가 명확하나 일부 부분에서 일관성이 떨어지거나 연결이 약합니다. 몇몇 문장 간의 통일성을 강화할 필요가 있습니다."),
                (1.0, "미흡합니다. 구조가 다소 혼란스럽고 일관성이 부족합니다. 몇몇 문장 간에는 연결이 있지만 전체적으로 조화롭지 않은 느낌을 줍니다."),
                (0.0, "매우 미흡합니다. 글의 구조가 혼란스럽고 무질서하며, 일관성이 없습니다. 문장 간의 연결이 부족합니다."),
            ]
        }

        feedback_list = model_feedback.get(self.model_name, [])

        for threshold, comment in feedback_list:
            if score >= threshold:
                return comment

        return "평가 점수 없음"
