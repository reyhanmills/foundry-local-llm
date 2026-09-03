# OpenAI client'ı kullanıyoruz.
# Foundry Local server OpenAI uyumlu API gibi çalışıyor.
from openai import OpenAI
import re


# Foundry Local server adresi.
client = OpenAI(
    base_url="http://127.0.0.1:51169/v1",
    api_key="not-needed"
)


# Cevap üretmek için kullanacağımız local LLM modeli.
MODEL_NAME = "qwen3-0.6b"


def clean_model_answer(answer):
    # Model <think>...</think> bloğu üretirse bu kısmı siliyoruz.
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)

    # Boşlukları temizliyoruz.
    answer = answer.strip()

    return answer


def generate_answer(question, context):
    system_message = """
Sen bir Türkçe Local RAG Assistant'sın.
Sadece verilen Context bilgisini kullan.
Kısa, net ve Türkçe cevap ver.
Düşünme süreci yazma.
<think> etiketi yazma.
"""

    user_message = f"""
Context:
{context}

Soru:
{question}

Sadece cevabı yaz:
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0,
        max_tokens=120
    )

    answer = response.choices[0].message.content
    cleaned_answer = clean_model_answer(answer)

    # Eğer model boş cevap döndürürse en azından context'e dayalı güvenli cevap veriyoruz.
    if not cleaned_answer:
        return f"Verilen context'e göre cevap: {context}"

    return cleaned_answer