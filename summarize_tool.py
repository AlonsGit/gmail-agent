
import sys
import json
import openai
import os

# Debug: check if API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not found in environment.", file=sys.stderr)
    raise EnvironmentError("Missing OPENAI_API_KEY environment variable")
else:
    print(f"✅ OPENAI_API_KEY loaded: {api_key[:8]}...", file=sys.stderr)

# Initialize OpenAI client (for openai>=1.0.0)
client = openai.OpenAI(api_key=api_key)

def gpt_summary(text):
    if not text.strip():
        return "No content to summarize."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes Hebrew business news."},
                {"role": "user", "content": f"סכם את הטקסט הבא בעברית בצורה תמציתית וברורה:\n{text}"}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    inputs = json.load(sys.stdin)
    text = inputs.get("text", "")
    summary = gpt_summary(text)
    print(json.dumps({"summary": summary}))

