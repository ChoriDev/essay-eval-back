import kss

def text_splitter(text, max_len):
    sentences = kss.split_sentences(text)
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