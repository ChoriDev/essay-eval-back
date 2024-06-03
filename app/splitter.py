import kss
from transformers import BertTokenizer

TARGET_MODEL = "klue/bert-base"
BERT_TOKENIZER = BertTokenizer.from_pretrained(TARGET_MODEL)

def split_by_up_to_400_characters(text):
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

def split_by_512_tokens(text):
    # 문장 단위로 텍스트 분할
    sentences = kss.split_sentences(text)
    max_len = 512
    current_chunk = []
    chunks = []
    current_len = 0

    for sentence in sentences:
        # 현재 문장을 토크나이징하여 토큰 개수 계산
        tokens = BERT_TOKENIZER.tokenize(sentence)
        tokens_len = len(tokens)

        # 현재 청크에 문장을 추가하였을 때 max_len 초과하는지 검사
        if current_len + tokens_len > max_len:
            # 초과하는 경우 현재 청크를 chunks에 추가하고 새 청크 시작
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_len = 0

        # 현재 청크에 문장 추가
        current_chunk.append(sentence)
        current_len += tokens_len

    # 마지막 청크 추가
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks