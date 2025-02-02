from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path):
    """Извлекает текст из PDF, объединяя все страницы."""
    reader = PdfReader(pdf_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def split_text_with_langchain(text, chunk_size=500, chunk_overlap=50):
    """Разбивает текст на чанки с перекрытием."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)
