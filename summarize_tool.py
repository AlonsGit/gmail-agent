
import sys
import json
import openai
import os

# Initialize OpenAI client (for openai>=1.0.0)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
