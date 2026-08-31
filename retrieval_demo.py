# JSON formatındaki embedding bilgisini tekrar Python listesine çevirmek için kullanıyoruz.
import json

# Matematiksel işlemler ve cosine similarity hesaplamak için numpy kullanıyoruz.
import numpy as np

# Veritabanındaki kayıtları okumak için database.py içinden fonksiyon alıyoruz.
from database import get_all_documents

# Kullanıcı sorusundan embedding üretmek için embedding_utils.py içinden fonksiyon alıyoruz.
from embedding_utils import generate_embedding


def cosine_similarity(vector_a, vector_b):
    # Liste olarak gelen embeddingleri numpy array formatına çeviriyoruz.
    a = np.array(vector_a)
    b = np.array(vector_b)

    # Cosine similarity formülü:
    # iki vektör arasındaki anlamsal benzerliği ölçer.
    similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    # Sonucu normal Python float olarak geri döndürüyoruz.
    return float(similarity)


def find_best_chunk(question):
    # Kullanıcının sorduğu soruyu embedding'e çeviriyoruz.
    question_embedding = generate_embedding(question)

    # Veritabanındaki tüm chunk kayıtlarını alıyoruz.
    documents = get_all_documents()

    # En iyi sonucu başlangıçta boş tutuyoruz.
    best_chunk = None
    best_score = -1

    # Her document kaydını tek tek geziyoruz.
    for document in documents:
        document_id = document[0]
        file_name = document[1]
        chunk_text = document[2]
        embedding_json = document[3]

        # Eğer embedding boşsa bu kaydı atlıyoruz.
        if embedding_json is None:
            continue

        # SQLite içinde TEXT olarak duran embedding'i tekrar Python listesine çeviriyoruz.
        chunk_embedding = json.loads(embedding_json)

        # Kullanıcı sorusu ile chunk arasındaki benzerliği hesaplıyoruz.
        score = cosine_similarity(question_embedding, chunk_embedding)

        # Eğer bu skor şimdiye kadarki en iyi skordan yüksekse sonucu güncelliyoruz.
        if score > best_score:
            best_score = score
            best_chunk = {
                "id": document_id,
                "file_name": file_name,
                "chunk_text": chunk_text,
                "score": score,
            }

    # En alakalı chunk sonucunu geri döndürüyoruz.
    return best_chunk


if __name__ == "__main__":
    # Kullanıcıdan terminal üzerinden soru alıyoruz.
    question = input("Sorunuz: ")

    # Soruyla en alakalı chunkı buluyoruz.
    result = find_best_chunk(question)

    # Sonucu terminale yazdırıyoruz.
    if result:
        print("En alakalı chunk:")
        print("Dosya:", result["file_name"])
        print("Skor:", result["score"])
        print("Metin:", result["chunk_text"])
    else:
        print("Alakalı bir chunk bulunamadı.")
        