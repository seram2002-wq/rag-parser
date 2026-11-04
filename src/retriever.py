from collections.abc import Sequence
from uuid import uuid4

from langchain_classic.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.documents import Document
from langchain_core.stores import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


def create_multi_vector_retriever(
    documents: Sequence[Document],
    *,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    collection_name: str = "multimodal_rag",
) -> MultiVectorRetriever:
    """Index child text chunks while returning their full parent documents."""
    if not documents:
        raise ValueError("At least one document is required.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    child_documents: list[Document] = []
    parent_ids: list[str] = []

    for document in documents:
        parent_id = str(uuid4())
        children = splitter.split_documents([document])
        for child in children:
            child.metadata["doc_id"] = parent_id
        child_documents.extend(children)
        parent_ids.append(parent_id)

    vectorstore = Chroma.from_documents(
        documents=child_documents,
        embedding=OpenAIEmbeddings(),
        collection_name=collection_name,
    )
    docstore = InMemoryStore()
    docstore.mset(list(zip(parent_ids, documents)))

    return MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=docstore,
        id_key="doc_id",
    )
