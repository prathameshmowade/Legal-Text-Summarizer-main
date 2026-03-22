from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ── PUT YOUR OPENROUTER API KEY HERE ──
# Get FREE key (no credit card): https://openrouter.ai → Sign Up → Keys
OPENROUTER_API_KEY = "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"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "Invalid JSON body."}), 400

        document_text = data.get("text", "").strip()
        if not document_text:
            return jsonify({"error": "No document text provided."}), 400

        prompt = (
            "You are an expert legal analyst. Summarize the following legal document clearly and concisely.\n\n"
            "Structure your response using these exact headings:\n\n"
            "**1. Document Type** - What kind of legal document this is.\n"
            "**2. Key Parties** - Names and roles of all parties involved.\n"
            "**3. Core Purpose** - The primary intent or objective of the document.\n"
            "**4. Key Clauses & Obligations** - Important terms, rights, and responsibilities.\n"
            "**5. Critical Dates & Deadlines** - Any relevant dates, timelines, or expiration.\n"
            "**6. Risks & Red Flags** - Potential issues, ambiguities, or concerns to be aware of.\n"
            "**7. Plain English Summary** - A 2-3 sentence layperson summary.\n\n"
            "Legal Document:\n\"\"\"\n"
            + document_text
            + "\n\"\"\""
        )

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://lexai.onrender.com",
            "X-Title": "LexAI Legal Summarizer",
        }

        payload = {
            # openrouter/free auto-picks the best available free model every time
            # It NEVER breaks even when individual models go down
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional legal analyst with deep expertise in "
                        "contract law, corporate law, and legal document review. "
                        "Be precise, structured, and use plain language where possible."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 1500,
            "temperature": 0.3,
        }

        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)

        if not resp.ok:
            try:
                err_msg = resp.json().get("error", {}).get("message", resp.text[:300])
            except Exception:
                err_msg = resp.text[:300]
            return jsonify({"error": f"API error ({resp.status_code}): {err_msg}"}), 502

        result = resp.json()
        summary = result["choices"][0]["message"]["content"]
        return jsonify({"summary": summary})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Please try again."}), 504

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Could not reach API. Check server connectivity."}), 503

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed."}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
