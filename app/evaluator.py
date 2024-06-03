import torch
from transformers import BertTokenizer, BertForSequenceClassification

class BertEvaluator:
    def __init__(self, model_path):
        target_model = "klue/bert-base"
        num_labels = 1
        self.tokenizer = BertTokenizer.from_pretrained(target_model)
        self.model = BertForSequenceClassification.from_pretrained(target_model, num_labels=num_labels)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

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