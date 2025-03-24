from flask import Flask, request, render_template
import os
from groq import Groq

app = Flask(__name__)

# Groq API Key (use env variable in production)
api_key = "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"
client = Groq(api_key=api_key)

@app.route('/')
def index():
    return render_template("index.html", result=None, image_url=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    image_url = request.form.get("image_url")

    if not image_url:
        return render_template("index.html", result="Please provide an image URL!", image_url=None)

    try:
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "the image is a waste and you are responsible to categorize it into either wet or dry. considering whatever is given and if it was supposed to be dumped, help in segregation being a waste manager. Reply in just one word, saying either dry or wet."
                        },
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            temperature=0,
            max_tokens=4,
            top_p=1.0,
            stream=False
        )

        # Extract classification result
        result = completion.choices[0].message.content.strip()
        return render_template("index.html", result=result, image_url=image_url)

    except Exception as e:
        return render_template("index.html", result=f"Error: {str(e)}", image_url=None)

if __name__ == "__main__":
    app.run(debug=True)
