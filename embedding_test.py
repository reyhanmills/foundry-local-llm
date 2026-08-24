# OpenAI client'ı kullanıyoruz.
# Foundry Local server, OpenAI uyumlu API gibi çalışabilir.
from openai import OpenAI


def main():
    # Foundry Local server adresi.
    # Senin terminalinde Web URL olarak bu adres göründü.
    client = OpenAI(
        base_url="http://127.0.0.1:52685/v1",
        api_key="not-needed"
    )

    # Embedding üretecek modelin adı.
    model_name = "qwen3-embedding-0.6b"

    # Test için embedding'e çevireceğimiz metin.
    text = "RAG, modelin cevap üretmeden önce belgelerden ilgili bilgiyi bulmasını sağlar."

    # Metni embedding'e çeviriyoruz.
    response = client.embeddings.create(
        model=model_name,
        input=text
    )

    # Dönen cevaptan embedding listesini alıyoruz.
    embedding = response.data[0].embedding

    # Embedding hakkında kısa bilgi yazdırıyoruz.
    print("Embedding başarıyla üretildi.")
    print("Embedding boyutu:", len(embedding))
    print("İlk 5 değer:", embedding[:5])


if __name__ == "__main__":
    main()