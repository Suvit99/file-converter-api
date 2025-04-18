from flask import Flask, request, send_file, jsonify
from PIL import Image
import os
import tempfile

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    if 'file' not in request.files or 'format' not in request.form:
        return jsonify({"error": "Missing file or format parameter"}), 400

    file = request.files['file']
    target_format = request.form['format'].lower()

    filename = file.filename.lower()

    # Save file to temp location
    with tempfile.NamedTemporaryFile(delete=False) as input_temp:
        file.save(input_temp.name)

        try:
            if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')):
                # Image file: convert using PIL
                img = Image.open(input_temp.name).convert('RGB')

                output_temp = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{target_format}')
                img.save(output_temp.name, target_format.upper())
                output_temp.close()

                return send_file(output_temp.name, as_attachment=True)

            else:
                return jsonify({"error": "Only image files can be converted in this version."}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            os.remove(input_temp.name)

if __name__ == "__main__":
    app.run(debug=True)
