from rag.loaders import (
    load_document
)

from rag.splitter import (
    split_documents
)

from rag.chroma_manager import (
    get_vectorstore
)


def ingest_file(
    file_path
):

    documents = load_document(
        file_path
    )

    chunks = split_documents(
        documents
    )

    vectorstore = (
        get_vectorstore()
    )

    vectorstore.add_documents(
        chunks
    )

    return {
        "chunks":
        len(chunks)
    }