import os
import requests
import gradio as gr

# 🔐 Insert your Hugging Face API key here or use environment variable
HF_API_KEY = os.environ.get("HF_API_KEY") 
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# 📌 Journal Analysis Function
def analyze_journal(journal_entry):
    if not journal_entry.strip():
        return "⚠ Please enter a journal entry."

    prompt = f"""
You are an emotional wellness expert and motivational coach.
Analyze the following journal entry:
\"\"\"{journal_entry}\"\"\"
Tasks:
1. Detect the emotional tone (e.g., happy, anxious, stressed, calm, etc.).
2. Identify any recurring themes or emotional patterns.
3. Suggest motivational advice personalized to the tone and themes.
Format your response in a clear and structured way.
"""

    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 500,
                "return_full_text": False
            }
        }
response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        generated_text = response.json()[0]['generated_text']
        return generated_text.strip()

    except Exception as e:
        return f"❌ Error during analysis: {str(e)}"

# 🧠 Gradio UI
interface = gr.Interface(
    fn=analyze_journal,
    inputs=gr.Textbox(label="📝 Enter your journal entry", lines=8, placeholder="Write your thoughts here..."),
    outputs=gr.Textbox(label="💡 Emotional Analysis + Motivation"),
    title="🧠 Mental Wellness Diary Analyzer",
    description="Analyze your journal",
)

# 🚀 Run
if _name_ == "_main_":
    interface.launch()
