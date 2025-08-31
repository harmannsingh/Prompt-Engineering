import requests
import google.generativeai as genai

# 🔐 Directly pasted API keys
CRICAPI_KEY = "3410c16201333dfc17ee12f47d55c0837036f2383519822428419c6b0a0c1eee"
GEMINI_API_KEY = "AIzaSyB-sys-YPEPBe1zOcMzSzk8kME6lcLcytU"


# 🧠 Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# 🔍 Get live cricket match info
def get_cricket_score():
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={CRICAPI_KEY}&offset=0"
    response = requests.get(url)
    
    try:
        data = response.json()
    except Exception:
        return None, "❌ Failed to parse response from CricAPI."

    if data.get("status") != "success":
        return None, f"❌ CricAPI Error: {data.get('message', 'Unknown error')}"

    matches = data.get("data", [])
    for match in matches:
        if match.get("matchStarted"):
            score = match.get('score', 'Score unavailable')
            status = match.get('status', 'No status provided')
            return f"{match['name']}:\nScore: {score}\nStatus: {status}", None

    return None, "ℹ️ No live matches available right now."

# 🧠 Ask Gemini to summarize
def summarize_with_gemini(text):
    prompt = f"Summarize this live cricket match:\n{text}"
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

# 🚀 Main Function
if __name__ == "__main__":
    print("🏏 LIVE CRICKET SUMMARY USING GEMINI\n")

    summary_text, error = get_cricket_score()

    if error:
        print(error)
    else:
        print("📦 Raw Match Info:\n" + summary_text)
        print("\n🧠 Gemini Summary:")
        print(summarize_with_gemini(summary_text))
