# OpenAI client'ı kullanıyoruz.
# Foundry Local server, OpenAI uyumlu API gibi çalışıyor.
from openai import OpenAI


# Foundry Local server adresi.
# Bu adres foundry server status çıktısında görülen local adrestir.
client = OpenAI(
    base_url="http://127.0.0.1:51169/v1",
    api_key="not-needed"
)


# Kullanacağımız embedding modeli.
MODEL_NAME = "qwen3-embedding-0.6b"


def generate_embedding(text):
    # Verilen metni embedding'e çeviriyoruz.
    response = client.embeddings.create(
        model=MODEL_NAME,
        input=text
    )

    # Dönen cevaptaki embedding listesini alıyoruz.
    embedding = response.data[0].embedding

    # Embedding listesini geri döndürüyoruz.
    return embedding