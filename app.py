import random
import string
import json
import os
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortened_urls = {}

# Load existing URLs from file if it exists
if os.path.exists("urls.json"):
    with open("urls.json", "r") as f:
        shortened_urls = json.load(f)

# Generate short URL
def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Home page - form and result
@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()

        # Ensure uniqueness
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url] = long_url

        # Save to file
        with open("urls.json", "w") as f:
            json.dump(shortened_urls, f)

    return render_template("index.html", short_url=short_url)

# Redirect to original URL
@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
