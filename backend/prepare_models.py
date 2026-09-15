"""Download model assets at build time so requests use local files."""
from pathlib import Path

import nltk
from sentence_transformers import SentenceTransformer


def main():
    backend = Path(__file__).resolve().parent
    nltk_dir = backend / "nltk_data"
    for package in ("stopwords", "punkt"):
        if not nltk.download(package, download_dir=str(nltk_dir), raise_on_error=True):
            raise RuntimeError(f"Failed to download NLTK package: {package}")

    model_dir = backend / "models" / "all-MiniLM-L6-v2"
    model_dir.parent.mkdir(parents=True, exist_ok=True)
    SentenceTransformer("all-MiniLM-L6-v2", device="cpu").save(str(model_dir))


if __name__ == "__main__":
    main()
