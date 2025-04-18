from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "File Converter API is Live!"

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    target_format = request.form['format']
    
    if not file:
        return "No file provided", 400

    img = Image.open(file.stream)
    output = io.BytesIO()
    img.save(output, format=target_format.upper())
    output.seek(0)

    filename = f"converted.{target_format.lower()}"
    return send_file(output, download_name=filename, as_attachment=True)
