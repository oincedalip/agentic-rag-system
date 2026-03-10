from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def load_documents(data_path: str):
    print(f"Processing data folder: {data_path}")

    docs = []

    for file in Path(data_path).glob("*"):
        print(f"Processing file {file}")

        if file.suffix == ".pdf":
            loader = PyPDFLoader(str(file))
            docs.extend(loader.load())

        elif file.suffix == ".txt":
            loader = TextLoader(str(file))
            docs.extend(loader.load())
        print("Processing DONE")

    return docs