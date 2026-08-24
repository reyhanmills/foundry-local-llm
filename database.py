# SQLite veritabanı ile çalışmak için Python'un hazır modülünü içe aktarıyoruz.
import sqlite3


# Veritabanı dosyamızın adı.
# Bu dosya proje klasörünün içinde oluşacak.
DB_NAME = "rag_assistant.db"


def create_database():
    # Veritabanına bağlanıyoruz.
    # Eğer rag_assistant.db dosyası yoksa, SQLite bunu otomatik oluşturur.
    connection = sqlite3.connect(DB_NAME)

    # Cursor, veritabanına SQL komutları göndermemizi sağlar.
    cursor = connection.cursor()

    # documents adında bir tablo oluşturuyoruz.
    # IF NOT EXISTS: Eğer tablo zaten varsa tekrar oluşturma demek.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            chunk_text TEXT NOT NULL
        )
    """)

    # Yapılan değişiklikleri veritabanına kaydediyoruz.
    connection.commit()

    # Veritabanı bağlantısını kapatıyoruz.
    connection.close()


def clear_documents():
    # Veritabanına bağlanıyoruz.
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # documents tablosundaki eski kayıtları siliyoruz.
    # Aynı belgeyi tekrar tekrar ekleyip kopya kayıt oluşturmak istemiyoruz.
    cursor.execute("DELETE FROM documents")

    # Silme işlemini kaydediyoruz.
    connection.commit()

    # Bağlantıyı kapatıyoruz.
    connection.close()


def save_chunk(file_name, chunk_text):
    # Veritabanına bağlanıyoruz.
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Bir chunk kaydı ekliyoruz.
    # ? işaretleri güvenli veri yerleştirmek için kullanılır.
    cursor.execute(
        "INSERT INTO documents (file_name, chunk_text) VALUES (?, ?)",
        (file_name, chunk_text)
    )

    # Ekleme işlemini kaydediyoruz.
    connection.commit()

    # Bağlantıyı kapatıyoruz.
    connection.close()


def get_all_documents():
    # Veritabanına bağlanıyoruz.
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # documents tablosundaki tüm kayıtları seçiyoruz.
    cursor.execute("SELECT id, file_name, chunk_text FROM documents")

    # Seçilen tüm kayıtları Python listesi olarak alıyoruz.
    rows = cursor.fetchall()

    # Veritabanı bağlantısını kapatıyoruz.
    connection.close()

    # Kayıtları geri döndürüyoruz.
    return rows


# Bu dosya direkt çalıştırılırsa create_database() fonksiyonu çalışır.
if __name__ == "__main__
    create_database()
    print("Database created successfully.")