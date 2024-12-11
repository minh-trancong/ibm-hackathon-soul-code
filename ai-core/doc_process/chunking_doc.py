import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

def chunk_docs(text, chunk_size=500, overlap=30):
    words = nltk.word_tokenize(text)
    if len(words) <= chunk_size:
        return [" ".join(words)]
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks