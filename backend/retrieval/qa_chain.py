from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


# -------------------------------
# LOAD VECTOR STORE
# -------------------------------

def get_vectorstore():
    embeddings = OpenAIEmbeddings()

    index_name = "oracle-insight-index"  # keep same as your Pinecone index

    vectorstore = Pinecone.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )

    return vectorstore


# -------------------------------
# CREATE QA CHAIN
# -------------------------------

def get_qa_chain():
    vectorstore = get_vectorstore()

    # retrieve more chunks (important)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o-mini"
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain


# -------------------------------
# MAIN FUNCTION
# -------------------------------

def ask_question(query: str):
    qa_chain = get_qa_chain()

    response = qa_chain.invoke({"query": query})

    docs = response.get("source_documents", [])

    # Extract meaningful chunks
    chunks = []
    pages = []

    for doc in docs:
        text = doc.page_content.strip()

        # keep chunk small and useful
        chunks.append(text[:200])

        if "page" in doc.metadata:
            pages.append(doc.metadata["page"])

    return {
        "main_points": chunks,
        "source_pages": list(set(pages))
    }