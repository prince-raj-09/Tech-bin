from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from groq import Groq

app = Flask(__name__)

# Uploads directory setup
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Replace with your actual Ngrok URL (run `ngrok http 5000` and copy the HTTPS URL)
NGROK_URL = "hhttps://675d-2402-e280-212a-60-fd0f-425c-9bef-f3a9.ngrok-free.app"

# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Home route (renders UI)
@app.route('/')
def index():
    return render_template("index.html")

# Handle image upload and classification
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Construct the public image URL for the API request
    image_url = f"{NGROK_URL}/uploads/{file.filename}"

    # Groq API key (Make sure this is valid)
    api_key = "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"
    client = Groq(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """You are an advanced AI waste classification system.

Analyze the given image and strictly classify the waste into one of the following categories:

Wet → Organic and biodegradable waste (food scraps, fruit peels, vegetable waste, garden waste).

Dry → Non-biodegradable waste (paper, cardboard, wood, glass, metals) excluding plastic and electronics.

Plastic → All plastic materials (bottles, wrappers, containers, synthetic packaging) and any unidentifiable waste, including electronics (E-Waste, circuit boards, wires, batteries, and devices).

Reply in one word."""
                        },
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            temperature=0,
            max_tokens=5,
            top_p=0.0,
            stream=False
        )

        # Extract classification result
        result = completion.choices[0].message.content.strip()
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)
