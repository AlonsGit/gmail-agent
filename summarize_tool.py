import sys
import json

def simple_summary(text):
    if not text.strip():
        return "No content to summarize."
    # Placeholder for LLM-based summarization
    return f"Summary: {text[:100].strip()}..."

if __name__ == '__main__':
    inputs = json.load(sys.stdin)
    text = inputs.get("text", "")
    summary = simple_summary(text)
    print(json.dumps({"summary": summary}))
