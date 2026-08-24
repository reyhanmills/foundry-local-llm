# database.py içindeki get_all_documents fonksiyonunu kullanıyoruz.
# Bu fonksiyon SQLite içindeki tüm chunkları getirir.
from database import get_all_documents


def calculate_similarity(question, chunk_text):
    # Kullanıcının sorusunu küçük harflere çeviriyoruz.
    question = question.lower()

    # Chunk metnini küçük harflere çeviriyoruz.
    chunk_text = chunk_text.lower()

    # Sorudaki kelimeleri parçalayarak bir kümeye çeviriyoruz.
    question_words = set(question.split())

    # Chunk içindeki kelimeleri parçalayarak bir kümeye çeviriyoruz.
    chunk_words = set(chunk_text.split())

    # Sorudaki ve chunk içindeki ortak kelimeleri buluyoruz.
    common_words = question_words.intersection(chunk_words)

    # Benzerlik skoru olarak ortak kelime sayısını kullanıyoruz.
    return len(common_words)


def find_best_chunk(question):
    # Veritabanındaki tüm chunkları alıyoruz.
    documents = get_all_documents()

    # En iyi sonucu saklamak için başlangıç değerleri.
    best_chunk = None
    best_score = 0

    # Her chunkı tek tek geziyoruz.
    for document in documents:
        # document yapısı şu şekilde:
        # (id, file_name, chunk_text)
        document_id = document[0]
        file_name = document[1]
        chunk_text = document[2]

        # Kullanıcı sorusu ile chunk arasındaki benzerliği hesaplıyoruz.
        score = calculate_similarity(question, chunk_text)

        # Eğer bu skor önceki en iyi skordan büyükse,
        # bu chunkı en iyi sonuç olarak kaydediyoruz.
        if score > best_score:
            best_score = score
            best_chunk = {
                "id": document_id,
                "file_name": file_name,
                "chunk_text": chunk_text,
                "score": score,
            }

    # En iyi chunkı geri döndürüyoruz.
    return best_chunk


if __name__ == "__main__":
    # Test için kullanıcıdan soru alıyoruz.
    question = input("Sorunuz: ")

    # Soruya en yakın chunkı buluyoruz.
    result = find_best_chunk(question)

    # Sonucu terminalde gösteriyoruz.
    if result:
        print("En alakalı chunk:")
        print("Dosya:", result["file_name"])
        print("Skor:", result["score"])
        print("Metin:", result["chunk_text"])
    else:
        print("Alakalı bir chunk bulunamadı.")