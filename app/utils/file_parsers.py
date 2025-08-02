# gijii-app\app\utils\file_parsers.py
from docx import Document
import fitz  # PyMuPDF

def parse_docx(file_content: bytes) -> str:
    """
    Word (docx) ファイルのバイトデータからテキストを抽出します。
    """
    try:
        # バイトデータをメモリ上のファイルとして開く
        from io import BytesIO
        doc = Document(BytesIO(file_content))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        return f"DOCX解析エラー: {e}"

def parse_pdf(file_content: bytes) -> str:
    """
    PDF ファイルのバイトデータからテキストを抽出します。
    """
    try:
        # バイトデータをメモリ上のファイルとして開く
        from io import BytesIO
        doc = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return f"PDF解析エラー: {e}"