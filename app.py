from flask import Flask, render_template, request, redirect, url_for
import requests
import base64
import os

app = Flask(__name__)

# 🔑 API KEY: Render me 'Environment Variables' me STABILITY_API_KEY naam se save karein
# Agar code me hi daalna hai toh yaha paste karein:
API_KEY = os.environ.get("STABILITY_API_KEY", "sk-terTFRp3OTFcOezTzu2yET1zU3lX6E8H2K3xYPvuLbOyICxY")

# Temporary memory database
gallery_db = []

def generate_image(prompt):
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "image/*"  # <--- Ye binary data mangne ke liye zaroori hai
    }

    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        # Binary content ko Base64 me convert kar rahe hain taaki HTML me dikhe
        return base64.b64encode(response.content).decode('utf-8')
    else:
        print("ERROR:", response.text)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_prompt = request.form.get("prompt")

        if user_prompt:
            image_data = generate_image(user_prompt)

            if image_data:
                # Nayi image list me sabse upar (index 0) add hogi
                gallery_db.insert(0, {
                    "prompt": user_prompt,
                    "image": image_data
                })

        return redirect(url_for("index"))

    return render_template("index.html", gallery=gallery_db)

if __name__ == "__main__":
    app.run(debug=True)
