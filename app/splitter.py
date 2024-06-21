import kss
from transformers import BertTokenizer

class TextSplitter:
    def __init__(self, target_model="klue/bert-base"):
        self.tokenizer = BertTokenizer.from_pretrained(target_model)

    def split_by_up_to_400_characters(self, text):
        sentences = kss.split_sentences(text)
        max_len = 400
        current_chunk = []
        chunks = []
        current_len = 0

        for sentence in sentences:
            sentence_len = len(sentence)
            if current_len + sentence_len > max_len:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_len = 0
            current_chunk.append(sentence)
            current_len += sentence_len

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def split_by_512_tokens(self, text):
        sentences = kss.split_sentences(text)
        max_len = 512
        current_chunk = []
        chunks = []
        current_len = 0

        for sentence in sentences:
            tokens = self.tokenizer.tokenize(sentence)
            tokens_len = len(tokens)

            if current_len + tokens_len > max_len:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_len = 0

            current_chunk.append(sentence)
            current_len += tokens_len

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks