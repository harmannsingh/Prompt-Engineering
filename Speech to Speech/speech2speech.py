import os
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from datetime import datetime

# 🔐 Set your Google AI Studio API key
GOOGLE_API_KEY = "AIzaSyB-sys-YPEPBe1zOcMzSzk8kME6lcLcytU"
genai.configure(api_key=GOOGLE_API_KEY)

# ⚡ Use Gemini 1.5 Flash model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# 📁 Output folder
OUTPUT_FOLDER = "s2s_recordings"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def listen_to_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("🔠 Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"\n📝 You said: {text}\n")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError:
        print("❌ Speech Recognition service error.")
        return ""

def get_gemini_response(prompt):
    try:
        print("🤖 Sending input to Gemini 1.5 Flash...")
        response = model.generate_content(prompt)
        reply = response.text.strip()
        print(f"\n💬 Gemini Response:\n{reply}\n")
        return reply
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return "I'm sorry, I couldn't generate a response."

def text_to_speech(text, filepath):
    tts = gTTS(text=text, lang='en')
    tts.save(filepath)
    print(f"🔊 Saved speech to {filepath}")

def play_audio(filepath):
    print(f"▶️ Playing: {filepath}")
    os.system(f'start {filepath}')  # Windows only

def save_conversation(input_text, response_text, text_file, input_audio_file, response_audio_file):
    with open(text_file, "w", encoding="utf-8") as f:
        f.write("👤 You said:\n" + input_text + "\n\n🤖 Gemini replied:\n" + response_text)
    print(f"💾 Saved conversation to '{text_file}'")
    print(f"🎧 Audio saved: '{input_audio_file}', '{response_audio_file}'")

def main():
    print("\n🔁 Gemini 1.5 Flash Speech-to-Speech Assistant\n")

    user_input = listen_to_microphone()
    if not user_input:
        return

    gemini_reply = get_gemini_response(user_input)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_audio_file = os.path.join(OUTPUT_FOLDER, f"input_{timestamp}.mp3")
    response_audio_file = os.path.join(OUTPUT_FOLDER, f"response_{timestamp}.mp3")
    text_file = os.path.join(OUTPUT_FOLDER, f"conversation_{timestamp}.txt")

    text_to_speech(user_input, input_audio_file)
    text_to_speech(gemini_reply, response_audio_file)

    save_conversation(user_input, gemini_reply, text_file, input_audio_file, response_audio_file)

    play_audio(response_audio_file)

    print("\n✅ All done. Files saved and response played.")
    return gemini_reply

if __name__ == "__main__":
    response = main()
    if response:
        print(f"\n📤 Returned Gemini Response: {response}")
