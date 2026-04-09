import os
from langchain_community.document_loaders import PyPDFLoader, UnstructuredFileLoader


def load_documents(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
        loader = UnstructuredFileLoader(file_path)

    return loader.load()