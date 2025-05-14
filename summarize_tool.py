import sys
import json

def simple_summary(text):
    if not text.strip():
        return "אין תוכן לסיכום."
    
    # מחזיר תקציר פשוט – התחלה של הטקסט (עד 120 תווים)
    return f"Summary: {text[:120].strip()}..."

if __name__ == '__main__':
    try:
        inputs = json.load(sys.stdin)
        text = inputs.get("text", "")
        summary = simple_summary(text)
        print(json.dumps({"summary": summary}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
