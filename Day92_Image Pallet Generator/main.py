# import image with PIL
# Convert to array with numpy
# use np.unique to find top 10 colors
# Add those colors to a new list
# Print list
from PIL import Image
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename

def quantize_color(rgb, step=32):
    # """Group similar colors by rounding values to the nearest multiple of 'step'."""
    r, g, b = rgb
    return (
        (r + step // 2) // step * step,
        (g + step // 2) // step * step,
        (b + step // 2) // step * step
    )

# img = Image.open("BUM.JPG").convert("RGB")

def top_colors(img):

    data = np.asarray(img)
    raw_data = []

    for row in data:
        for px in row:
            rgb_tuple = tuple(int(value) for value in px)
            raw_data.append(rgb_tuple)

    quantized_list = [quantize_color(color, step=32) for color in raw_data]

    data_series = pd.Series(data=quantized_list)

    top_10 = data_series.value_counts().head(10).index.tolist()

    return top_10

# Flask uses Jinja through render_template().
# Bootstrap is added in your HTML template with a CDN <link>, not imported in Python.

# Left, ask for image. Display image
# right, display output from function using cards and colors
# profit


app = Flask(__name__)

APP_DIR = Path(__file__).parent
UPLOAD_FOLDER = APP_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    image_filename = None
    colors = []

    if request.method == "POST":
        uploaded_file = request.files.get("image")

        if uploaded_file and uploaded_file.filename:
            original_filename = secure_filename(uploaded_file.filename)
            file_extension = Path(original_filename).suffix.lower()
            image_filename = f"{uuid4().hex}{file_extension}"
            image_path = UPLOAD_FOLDER / image_filename
            uploaded_file.save(image_path)

            img = Image.open(image_path).convert("RGB")
            colors = top_colors(img)

    return render_template("index.html", image_filename=image_filename, colors=colors)

# @app.route("/")
# def home():
#     colors = [(128, 128, 96), (32, 32, 32), (96, 96, 64), (128, 128, 128), (128, 96, 64), (64, 64, 32), (160, 160, 128), (160, 128, 96), (128, 96, 96), (64, 64, 64)]
#     return render_template("index.html", colors=colors)

if __name__ == "__main__":
    app.run(debug=True)
