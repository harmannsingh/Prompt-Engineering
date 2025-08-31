import os
import numpy as np
from tkinter import Tk, filedialog
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai

# ---------- ENTER YOUR GEMINI API KEY ----------
GEMINI_API_KEY = "AIzaSyB-sys-YPEPBe1zOcMzSzk8kME6lcLcytU"

# ✅ Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# 📤 Select PDF using file dialog
def upload_pdf():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

# 📄 Extract text from PDF
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

# 🧩 Split text into paragraphs
def split_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

# 🧠 Retrieve top relevant chunks using cosine similarity
def retrieve_relevant_chunks(query, chunks, top_k=3):
    documents = chunks + [query]
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()

    query_vec = vectors[-1]
    doc_vectors = vectors[:-1]

    scores = cosine_similarity([query_vec], doc_vectors)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]

    return [chunks[i] for i in top_indices]

# 🤖 Generate response using Gemini
def generate_answer(query, context):
    prompt = f"""Use the following context to answer the question.\n
Context:\n{context}\n\n
Question: {query}
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# 🔁 Main Execution
if __name__ == "__main__":
    print("📤 Upload a PDF file...")
    pdf_path = upload_pdf()

    if not pdf_path:
        print("❌ No file selected.")
        exit()

    print(f"📄 Extracting text from: {os.path.basename(pdf_path)}")
    text = extract_text_from_pdf(pdf_path)

    print("🧩 Splitting into chunks...")
    chunks = split_into_chunks(text)

    print("\n✅ You can now ask questions from the PDF (type 'exit' to quit):")
    while True:
        query = input("\n❓ Your Question: ")
        if query.lower() == "exit":
            break
        top_chunks = retrieve_relevant_chunks(query, chunks)
        context = "\n---\n".join(top_chunks)
        answer = generate_answer(query, context)
        print(f"\n🤖 Gemini Answer:\n{answer}")
