import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_unstructured import UnstructuredLoader


def extract_pdf(
    pdf_path: str | Path,
    *,
    strategy: str = "fast",
    chunking_strategy: str = "by_title",
    max_characters: int = 1000,
) -> list[Document]:
    """Partition a PDF through the Unstructured API and return LangChain documents."""
    load_dotenv()

    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    api_key = os.getenv("UNSTRUCTURED_API_KEY")
    api_url = os.getenv("UNSTRUCTURED_API_URL")
    if not api_key or not api_url:
        raise RuntimeError("Set UNSTRUCTURED_API_KEY and UNSTRUCTURED_API_URL in .env.")

    loader = UnstructuredLoader(
        file_path=str(path),
        api_key=api_key,
        url=api_url,
        partition_via_api=True,
        strategy=strategy,
        chunking_strategy=chunking_strategy,
        max_characters=max_characters,
    )
    return loader.load()
