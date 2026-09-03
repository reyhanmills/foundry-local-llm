# Retrieval işlemi için find_best_chunk fonksiyonunu kullanıyoruz.
from retrieval import find_best_chunk

# Cevap üretmek için generate_answer fonksiyonunu kullanıyoruz.
from answer_generator import generate_answer


def main():
    print("Local RAG Assistant başlatıldı.")
    print("Çıkmak için 'exit' veya 'quit' yazabilirsin.")
    print("-" * 40)

    # Kullanıcı çıkış yazana kadar soru sormaya devam eder.
    while True:
        # Kullanıcıdan soru alıyoruz.
        question = input("\nSorunuz: ")

        # Kullanıcı çıkmak isterse döngüyü bitiriyoruz.
        if question.lower() in ["exit", "quit", "çıkış"]:
            print("Local RAG Assistant kapatıldı.")
            break

        # Boş soru girilirse kullanıcıyı uyarıyoruz.
        if not question.strip():
            print("Lütfen bir soru yaz.")
            continue

        # Soruyla en alakalı chunkı buluyoruz.
        result = find_best_chunk(question)

        # Eğer alakalı chunk bulunursa cevap üretiyoruz.
        if result:
            answer = generate_answer(question, result["chunk_text"])

            print("\nCevap:")
            print(answer)

            print("\nKaynak:")
            print("Dosya:", result["file_name"])
            print("Skor:", result["score"])
            print("Metin:", result["chunk_text"])
        else:
            print("Alakalı bir chunk bulunamadı.")


if __name__ == "__main__":
    main()