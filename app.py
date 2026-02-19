from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# 🔑 PUT YOUR NEW REAL API KEY HERE
STABILITY_API_KEY = "sk-terTFRp3OTFcOezTzu2yET1zU3lX6E8H2K3xYPvuLbOyICxY"

# Temporary memory database
gallery_db = []

def generate_image(prompt):
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json"
    }

    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        print("ERROR:", response.text)
        return None

    data = response.json()
    return data["image"]  # base64 image


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_prompt = request.form.get("prompt")

        if user_prompt:
            image_data = generate_image(user_prompt)

            if image_data:
                gallery_db.insert(0, {
                    "prompt": user_prompt,
                    "image": image_data
                })

        return redirect(url_for("index"))

    return render_template("index.html", gallery=gallery_db)


if __name__ == "__main__":
    app.run(debug=True)
