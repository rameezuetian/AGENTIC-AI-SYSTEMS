from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)

loader = PyPDFLoader(
    "data/syllabus.pdf"
)

docs = loader.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(
    docs
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)
vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

vectorstore.save_local(
    "vectorstore"
)