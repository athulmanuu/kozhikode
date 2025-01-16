from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import google.generativeai as genai
import cv2
import base64
import numpy as np
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Create a templates directory and put your HTML file there
app.template_folder = 'templates'

# Configure Gemini AI
genai.configure(api_key="AIzaSyDq0yhNLsIyej11aG2FUAnX0qNNSAmzfic")
model = genai.GenerativeModel("gemini-1.5-pro")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    try:
        # Get the image data from the request
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({'error': 'No image data received'}), 400

        # Remove the data URL prefix if present
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]

        # Generate caption using Gemini
        prompt = "is this object plastic or not,if the object is plastic only say ' you got 10 reward points'"
        response = model.generate_content([
            {'mime_type': 'image/jpeg', 'data': image_data},
            prompt
        ])

        return jsonify({'result': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)