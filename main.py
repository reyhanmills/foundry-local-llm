# Dosya ve klasörlerle çalışmak için Path aracını kullanıyoruz.
from pathlib import Path

# database.py içindeki fonksiyonları bu dosyada kullanmak için içe aktarıyoruz.
from database import create_database, clear_documents, save_chunk, get_all_documents


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

        # Her chunkı hem terminale yazdırıyoruz hem de veritabanına kaydediyoruz.
        for index, chunk in enumerate(chunks, start=1):
            print(f"Chunk {index}: {chunk}")

            # Chunkı SQLite veritabanına kaydediyoruz.
            save_chunk(file_path.name, chunk)

    print("Chunklar veritabanına kaydedildi.")

    # Veritabanına kaydedilen kayıtları tekrar okuyoruz.
    saved_documents = get_all_documents()

    # Kaç kayıt olduğunu terminale yazdırıyoruz.
    print("Veritabanındaki kayıt sayısı:", len(saved_documents))

    # Veritabanındaki her kaydı terminale yazdırıyoruz.
    for document in saved_documents:
        print(document)


if __name__ == "__main__":
    main()