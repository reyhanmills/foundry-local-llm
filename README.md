# Local RAG Assistant MVP

Local RAG Assistant, metin belgeleri üzerinde çalışan Türkçe bir soru-cevap uygulamasıdır. Embedding ve cevap üretimi bilgisayarda Foundry Local üzerinden yerel olarak yapılır.

## Uygulama ne yapar?

- `documents` klasöründeki `.txt` dosyalarını okur.
- Metinleri satır bazlı küçük parçalara (chunk) ayırır.
- Chunk'ları ve embedding'lerini SQLite veritabanında saklar.
- Soruyla en alakalı chunk'ı embedding benzerliğiyle bulur.
- Yerel LLM ile bulunan context'e dayalı Türkçe cevap üretir.
- Cevabı ve kaynak bilgisini interaktif CLI'da gösterir.

## Teknolojiler

- Python
- Foundry Local
- OpenAI uyumlu yerel API
- SQLite
- NumPy
- Embedding modeli: `qwen3-embedding-0.6b`
- Chat modeli: `qwen3-0.6b`

## RAG akışı

```text
documents/*.txt
      ↓
Metni chunk'lara ayırma
      ↓
Embedding üretme ve SQLite'a kaydetme
      ↓
Kullanıcı sorusunun embedding'ini üretme
      ↓
En benzer chunk'ı bulma
      ↓
Yerel LLM ile cevap üretme
      ↓
CLI'da cevap ve kaynağı gösterme
```

## Kurulum ve çalıştırma

Python ortamını hazırlayın:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Foundry Local sunucusunu başlatın ve modelleri hazırlayın:

```bash
foundry server start
foundry model download qwen3-embedding-0.6b
foundry model download qwen3-0.6b
foundry model load qwen3-embedding-0.6b
foundry model load qwen3-0.6b
foundry server status
```

Ardından belgeleri indeksleyin ve CLI'ı çalıştırın:

```bash
python main.py
python rag_cli.py
```

Sorunuzu yazın. Uygulamayı kapatmak için `exit`, `quit` veya `çıkış` yazabilirsiniz.

> Foundry Local API adresi değişirse `config.py` içindeki `FOUNDRY_BASE_URL` değerini güncelleyin.

## Demo soruları

Mevcut `documents/sample.txt` dosyasıyla şunları deneyebilirsiniz:

- Foundry Local nedir?
- RAG ne işe yarar?
- SQLite bu projede ne için kullanılıyor?

## MVP durumu

MVP; belge indeksleme, SQLite'a kayıt, embedding tabanlı retrieval, yerel modelle cevap üretme, kaynak gösterme ve temel Foundry Local hata mesajlarını içerir. Şu anda uygulama interaktif CLI üzerinden çalışır; web arayüzü yoktur.
