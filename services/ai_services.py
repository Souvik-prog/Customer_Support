import os
from config import ANTHROPIC_API_KEY, OPENAI_API_KEY, PDF_CONTEXT_PATH

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate


class ClaudeService:
    """A service class to encapsulate the Claude API logic with RAG."""

    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable not set (required for embeddings).")

        self.llm = ChatAnthropic(model="claude-3-haiku-20240307", api_key=ANTHROPIC_API_KEY)
        self.retriever = self._initialize_retriever()
        self.rag_chain = self._create_rag_chain()

    def _initialize_retriever(self):
        if not os.path.exists(PDF_CONTEXT_PATH):
            print(f"Warning: PDF file not found at '{PDF_CONTEXT_PATH}'. The AI will not have context.")
            return None

        print("Loading and processing PDF for context...")

        loader = PyPDFLoader(PDF_CONTEXT_PATH)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

        print("PDF processed successfully.")
        return vectorstore.as_retriever()

    def _create_rag_chain(self):
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know. "
            "Keep the answer concise and helpful."
            "\n\n"
            "{context}"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        return create_retrieval_chain(self.retriever, question_answer_chain)

    def get_response(self, user_prompt: str) -> str:
        if not self.retriever:
            return "I'm sorry, my knowledge base document is missing. I cannot answer your question."

        try:
            response = self.rag_chain.invoke({"input": user_prompt})
            return response.get("answer", "I could not find an answer in the document.")
        except Exception as e:
            print(f"Error during RAG chain invocation: {e}")
            return "I had a problem processing your request with the AI. Please try again."

claude_service = ClaudeService()

