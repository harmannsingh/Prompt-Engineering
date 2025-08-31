#!C:\Users\harma\Desktop\python\myenv\Scripts\python.exe
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Configure Gemini API

API_KEY = "AIzaSyB-sys-YPEPBe1zOcMzSzk8kME6lcLcytU"
genai.configure(api_key=API_KEY)

# Initialize Gemini Model with System Prompt

model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash-lite",
    system_instruction="You are a helpful summarizer bot. Your job is to read website content and create a clean, concise summary in markdown format with headings and bullet points."
)

# Fetch Website Content & Extract Links

def fetch_website_text_and_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Clean up unwanted tags
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()

        text = soup.get_text(separator=' ', strip=True)

        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc

        internal_links = set()
        external_links = set()

        for link_tag in soup.find_all('a', href=True):
            href = link_tag['href']
            full_url = urljoin(url, href)
            if base_domain in urlparse(full_url).netloc:
                internal_links.add(full_url)
            else:
                external_links.add(full_url)

        return text, sorted(internal_links), sorted(external_links)

    except Exception as e:
        return f"Error fetching website: {e}", [], []

# Generate Summary

def summarize_website_content(url, content):
    prompt = f"""
    Please summarize the following website content in *Markdown format* with:
    - Headings
    - Bullet points where needed
    - Simple, clean language

    Website URL: {url}

    Content:
    {content[:15000]}
    """
    response = model.generate_content(prompt)
    return response.text

# Save Markdown to File

def save_summary(markdown_text, filename="summary.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    print(f"\n✅ Summary saved to: {filename}")

# Display Links

def display_links(internal_links, external_links):
    print("\n🔗 Internal Links:")
    for link in internal_links:
        print("  -", link)

    print("\n🌐 External Links:")
    for link in external_links:
        print("  -", link)

# Main Loop

def main():
    print("🌐 Website Summarizer Chatbot (Gemini 2.0 Flash Lite)")
    while True:
        url = input("\n🔗 Enter website URL to summarize: ").strip()
        print("\n⏳ Fetching content and links...")

        content, internal_links, external_links = fetch_website_text_and_links(url)

        if content.startswith("Error"):
            print(content)
        else:
            print("\n⏳ Generating summary...\n")
            summary = summarize_website_content(url, content)
            print("\n📄 Summary (Markdown Format):\n")
            print(summary)
            save_summary(summary)

            # Show Internal and External Links

            display_links(internal_links, external_links)

        again = input("\n🔁 Do you want to summarize another website? (yes/no): ").strip().lower()
        if again != "yes":
            print("👋 Thank you! Exiting.")
            break

if __name__ == "__main__":
    main()