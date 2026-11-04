import os
from collections.abc import Sequence

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


def summarize_documents(
    documents: Sequence[Document],
    *,
    model: str | None = None,
) -> str:
    """Summarize document text using the configured OpenAI chat model."""
    if not documents:
        raise ValueError("At least one document is required.")

    load_dotenv()
    llm = ChatOpenAI(
        model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
    )
    content = "\n\n".join(document.page_content for document in documents)
    response = llm.invoke(
        [
            SystemMessage(content="Summarize the source documents accurately and concisely."),
            HumanMessage(content=content),
        ]
    )
    return str(response.content)
