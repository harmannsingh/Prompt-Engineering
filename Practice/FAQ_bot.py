import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ✅ Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Format prompt like Langflow block
def format_prompt(user_question):
    return f"""
You are a helpful FAQ assistant. 
Answer the following question in a simple and clear manner.

Question: {user_question}

Answer:
"""

# ✅ Handle submit button
def handle_submit():
    question = entry.get()
    if not question.strip():
        return

    prompt = format_prompt(question)
    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
    except Exception as e:
        answer = f"❌ Error: {e}"

    output.insert(tk.END, f"🟢 You: {question}\n🤖 Bot: {answer}\n\n")
    entry.delete(0, tk.END)

# ✅ GUI Setup
root = tk.Tk()
root.title("Gemini FAQ Bot")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=60, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=5)
entry.bind("<Return>", lambda event: handle_submit())

submit_button = tk.Button(frame, text="Ask", command=handle_submit)
submit_button.pack(side=tk.LEFT)

output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Arial", 11))
output.pack(pady=10)
output.insert(tk.END, "🤖 Gemini FAQ Bot\n\n")

root.mainloop()
