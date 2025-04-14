import os
import requests
import gradio as gr

# 🔐 Hugging Face API Key: fallback to direct key if env var isn't set
HF_API_KEY = os.environ.get("HF_API_KEY") or "hf_your_actual_key_here"  # Replace with your key if testing locally
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# 📌 Journal Analysis Function
def analyze_journal(journal_entry):
    if not journal_entry.strip():
        return "⚠ Please enter a journal entry."

    # Prompt for the LLM
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

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 500,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        response_data = response.json()

        if isinstance(response_data, list) and "generated_text" in response_data[0]:
            return response_data[0]['generated_text'].strip()
        else:
            return "⚠ Unexpected response format from model."

    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP error: {http_err}"
    except Exception as e:
        return f"❌ Error during analysis: {str(e)}"

# 🧠 Gradio UI
interface = gr.Interface(
    fn=analyze_journal,
    inputs=gr.Textbox(
        label="Enter your journal entry",
        lines=8,
        placeholder="Write your thoughts here..."
    ),
    outputs=gr.Textbox(
        label="Emotional Analysis + Motivation"
    ),
    title="Mental Wellness Diary Analyzer",
    description="Enter your daily journal or diary entry and get an emotional analysis with motivational advice."
)

# 🚀 Run
if __name__ == "__main__":
    interface.launch(share=True)
