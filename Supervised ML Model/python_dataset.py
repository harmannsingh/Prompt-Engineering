import pandas as pd
import json

# 🧠 System Prompt
system_prompt = "You are an expert Python developer."

# 🔤 Define dataset
dataset = [
    {
        "user": "Create a function to calculate factorial.",
        "response": "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)"
    },
    {
        "user": "Write a function to reverse a string.",
        "response": "def reverse_string(s):\n    return s[::-1]"
    },
    {
        "user": "Check if a number is prime.",
        "response": "def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0: return False\n    return True"
    },
    {
        "user": "Find the largest number in a list.",
        "response": "def find_max(lst):\n    return max(lst)"
    },
    {
        "user": "Count the vowels in a string.",
        "response": "def count_vowels(s):\n    return sum(1 for c in s.lower() if c in 'aeiou')"
    }
]

# 💾 Save as CSV
df = pd.DataFrame(dataset)
df["system"] = system_prompt
df = df[["system", "user", "response"]]
df.to_csv("dataset.csv", index=False)
print("[✔] Saved dataset.csv")

# 📦 Prepare for JSONL
jsonl_data = [
    {
        "input": f"<system>\n{row['system']}\n<user>\n{row['user']}",
        "output": row["response"]
    }
    for _, row in df.iterrows()
]

# 🔀 Split 80-20
split = int(0.8 * len(jsonl_data))
train, test = jsonl_data[:split], jsonl_data[split:]

# 💾 Save as JSONL
with open("train.jsonl", "w") as f:
    for item in train:
        f.write(json.dumps(item) + "\n")
print("[✔] Saved train.jsonl")

with open("test.jsonl", "w") as f:
    for item in test:
        f.write(json.dumps(item) + "\n")
print("[✔] Saved test.jsonl")