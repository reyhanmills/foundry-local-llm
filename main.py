from pathlib import Path

#main fonksiyonu tanımlıyorum
#belgelerin konumunu belirliyorum ve .txt ile biten tum belgeleri alıyoeuz.
#turkçe karakterler bozulmasın diye utf-8
def main(): 
    documents_folder = Path("documents")
    for file_path in documents_folder.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")
        print("Dosya adı:", file_path.name)
        print("Dosya içeriği:")
        print(content)


if __name__ == "__main__":
    main()

    #bu dosya çalışırsa main fonksiyonunu çalıştır.