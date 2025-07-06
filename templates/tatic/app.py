from flask import Flask, request, jsonify, render_template
import openai
import tempfile
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio = request.files["audio"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp:
        audio.save(temp.name)
        transcript_response = openai.Audio.transcribe("whisper-1", open(temp.name, "rb"))
        transcript = transcript_response["text"]

    # Prompt dla GPT
    prompt = f"""Jesteś AI-asystentem handlowca. Na podstawie rozmowy:
{transcript}

Wygeneruj:
1. Trzy pytania dopasowane do sytuacji klienta i etapu rozmowy.
2. Dwie sugestie coachingowe dla handlowca: tempo, ton, zaangażowanie klienta.
"""

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    output = completion["choices"][0]["message"]["content"]
    questions, coaching = output.split("\n\n", 1)

    return jsonify({
        "transcript": transcript,
        "questions": questions,
        "coaching": coaching
    })

if __name__ == "__main__":
    app.run(debug=True)
