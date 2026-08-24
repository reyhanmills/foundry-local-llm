from pathlib import Path


def split_into_chunks(text):
    chunks = []

    for line in text.splitlines():
        cleaned_line = line.strip()

        if cleaned_line:
            chunks.append(cleaned_line)

    return chunks


def main():
    documents_folder = Path("documents")

    for file_path in documents_folder.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")
        chunks = split_into_chunks(content)

        print("Dosya adı:", file_path.name)
        print("Chunk sayısı:", len(chunks))

        for index, chunk in enumerate(chunks, start=1):
            print(f"Chunk {index}: {chunk}")


if __name__ == "__main__":
    main()