
import time
import google.generativeai as genai

# 🔐 Configure your API key
genai.configure(api_key="AIzaSyB-sys-YPEPBe1zOcMzSzk8kME6lcLcytU")  # Replace with your key

# ⚡ Load Gemini 1.5 Flash
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def safe_generate_content(prompt: str, retries=3, wait=60) -> str:
    """
    Retry mechanism for handling 429 (quota exceeded) or transient errors.
    """
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                print(f"⚠ Quota limit hit. Retrying in {wait} seconds... ({attempt + 1}/{retries})")
                time.sleep(wait)
            else:
                return f"❌ Error: {e}"
    return "❌ Error: Quota limit reached after multiple retries."

def classify_text(text: str) -> str:
    prompt = f"""
Please classify the following text into one of these categories: Sports, Politics, or Technology.

Text: "{text}"
"""
    return safe_generate_content(prompt)

def generate_story(prompt_text: str) -> str:
    prompt = f"""
Write a short fictional story based on the prompt below:

Prompt: {prompt_text}
"""
    return safe_generate_content(prompt)

# 🚀 Main Program
def main():
    print("🔷 Welcome to the Gemini AI Text Tool")
    print("Choose task:\n1. Text Classification\n2. Text Generation")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        user_text = input("Enter text to classify (e.g., a news sentence):\n> ")
        result = classify_text(user_text)
        print(f"\n🧠 Predicted Category: {result}")

    elif choice == "2":
        story_prompt = input("Enter your story prompt:\n> ")
        result = generate_story(story_prompt)
        print(f"\n📖 Generated Story:\n{result}")

    else:
        print("❌ Invalid option. Please enter 1 or 2.")

# ✅ Corrected __main__ block
if __name__ == "__main__":
    main()
