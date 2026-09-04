import streamlit as st
from openai import APIConnectionError, BadRequestError, NotFoundError

from answer_generator import generate_answer
from retrieval import find_best_chunk


st.set_page_config(page_title="Local RAG Assistant")

st.title("Local RAG Assistant")
st.write(
    "Yerel belgelerden ilgili bilgiyi bulan ve Foundry Local modelleriyle "
    "Türkçe cevap üreten basit bir RAG uygulaması."
)

question = st.text_input("Sorunuz")

if st.button("Cevap Üret"):
    if not question.strip():
        st.warning("Lütfen bir soru yazın.")
    else:
        try:
            with st.spinner("Cevap hazırlanıyor..."):
                result = find_best_chunk(question)

                if result:
                    answer = generate_answer(question, result["chunk_text"])

            if result:
                st.subheader("Cevap")
                st.write(answer)

                st.subheader("Kaynak")
                st.write("Dosya adı:", result["file_name"])
                st.write("Benzerlik skoru:", f'{result["score"]:.4f}')
                st.write("Chunk metni:", result["chunk_text"])
            else:
                st.info("Alakalı bir chunk bulunamadı.")
        except APIConnectionError:
            st.error(
                "Foundry Local server çalışmıyor. "
                "Lütfen önce `foundry server start` çalıştır."
            )
        except (NotFoundError, BadRequestError):
            st.error(
                "Gerekli model load edilmemiş. "
                "Lütfen embedding ve chat modellerini tekrar load et."
            )
