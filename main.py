# Dosya ve klasörlerle çalışmak için Path aracını kullanıyoruz.
from pathlib import Path

# database.py içindeki fonksiyonları bu dosyada kullanmak için içe aktarıyoruz.
from database import create_database, clear_documents, save_chunk, get_all_documents

# embedding_utils.py içindeki embedding üretme fonksiyonunu kullanıyoruz.
from embedding_utils import generate_embedding


def split_into_chunks(text):
    # Chunkları saklamak için boş bir liste oluşturuyoruz.
    chunks = []

    # Metni satır satır geziyoruz.
    for line in text.splitlines():
        # Satırın başındaki ve sonundaki boşlukları temizliyoruz.
        cleaned_line = line.strip()

        # Eğer satır boş değilse listeye ekliyoruz.
        if cleaned_line:
            chunks.append(cleaned_line)

    # Hazırlanan chunk listesini geri döndürüyoruz.
    return chunks


def main():
    # Önce veritabanını ve tabloyu hazır hale getiriyoruz.
    create_database()

    # Eski kayıtları temizliyoruz.
    # Böylece programı tekrar çalıştırınca aynı chunklar tekrar tekrar eklenmez.
    clear_documents()

    # Belgelerin bulunduğu klasörü seçiyoruz.
    documents_folder = Path("documents")

    # documents klasöründeki tüm .txt dosyalarını geziyoruz.
    for file_path in documents_folder.glob("*.txt"):
        # Dosyanın içeriğini okuyoruz.
        content = file_path.read_text(encoding="utf-8")

        # Dosyanın içeriğini chunklara bölüyoruz.
        chunks = split_into_chunks(content)

        print("Dosya adı:", file_path.name)
        print("Chunk sayısı:", len(chunks))

        # Her chunk için embedding üretip veritabanına kaydediyoruz.
        for index, chunk in enumerate(chunks, start=1):
            print(f"Chunk {index}: {chunk}")

            # Chunk için embedding üretiyoruz.
            embedding = generate_embedding(chunk)

            # Chunkı ve embedding bilgisini SQLite veritabanına kaydediyoruz.
            save_chunk(file_path.name, chunk, embedding)

    print("Chunklar veritabanına kaydedildi.")

    # Veritabanına kaydedilen kayıtları tekrar okuyoruz.
    saved_documents = get_all_documents()

    # Sadece kayıt sayısını terminale yazdırıyoruz.
    # Embedding değerlerini yazdırmıyoruz çünkü çok uzunlar.
    print("Veritabanındaki kayıt sayısı:", len(saved_documents))


if __name__ == "__main__":
    main()