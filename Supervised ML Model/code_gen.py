import google.generativeai as genai

# 🔐 Directly enter your Gemini API key here
api_key = "AIzaSyB-sys-YPEPBe1zOcMzSzk8kME6lcLcytU"  # Replace with your real API key

# ✅ Configure the API key
genai.configure(api_key=api_key)

# ✅ Use Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_code(system_prompt, user_prompt):
    """Generate code based on user prompt"""
    prompt = f"{system_prompt}\n\n{user_prompt}"
    response = model.generate_content(prompt)
    return response.text

def optimize_code(code):
    """Ask Gemini to optimize the given code"""
    prompt = f"You are an expert Python developer. Optimize the following code:\n\n{code}"
    response = model.generate_content(prompt)
    return response.text

def debug_code(code):
    """Ask Gemini to debug the given code"""
    prompt = f"You are an expert Python developer. Debug the following code and provide corrected code with explanation if needed:\n\n{code}"
    response = model.generate_content(prompt)
    return response.text

# ✅ Main Execution
if __name__ == "__main__":
    system_prompt = "You are an expert Python developer."
    user_prompt = input("📝 Enter your code prompt: ")

    print("\n🤖 Generating Code...\n")
    code = generate_code(system_prompt, user_prompt)
    print("🧠 Generated Code:\n")
    print(code)

    # ✅ Ask for optimization
    optimize_choice = input("\n⚙ Do you want to optimize this code? (yes/no): ").strip().lower()
    if optimize_choice == "yes":
        print("\n🔧 Optimizing Code...\n")
        code = optimize_code(code)
        print("🚀 Optimized Code:\n")
        print(code)
    else:
        print("✅ Skipping optimization.")

    # ✅ Ask for debugging
    debug_choice = input("\n🛠 Do you want to debug this code? (yes/no): ").strip().lower()
    if debug_choice == "yes":
        print("\n🔍 Debugging Code...\n")
        code = debug_code(code)
        print("✅ Debugged Code:\n")
        print(code)
    else:
        print("✅ Skipping debugging.")
