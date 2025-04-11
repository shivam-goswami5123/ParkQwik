# import os
# from flask import Flask, request, render_template, jsonify
# from dotenv import load_dotenv
# import google.generativeai as genai
# from PIL import Image
# import io
#
# # Load environment variables
# load_dotenv()
#
# # Initialize Flask app
# app = Flask(__name__)
#
#
# prompt = """
#
# Role: You are a vigilant security guard responsible for monitoring a parking lot.
#
# Task: Analyze the given parking lot image based on the following rules:
# 1. Proper Parking: Each car must be fully within the boundaries of a single parking space. No car should extend into another space significantly.
# 2. Line Crossing: Minor overlap of parking lines is acceptable, but excessive crossing that obstructs adjacent spaces is not.
# 3. Space Conflict: No two cars should be parked in the same designated parking spot.
#
# Analysis Flow:
# 1. First, identify and analyze the parking lines carefully.
# 2. Then, determine whether each car is parked correctly based on the rules above.
#
# Response:
# 1. Return FALSE if all cars comply with the rules (No major action needed).
# 2. Return TRUE if any rule is significantly violated (Major action needed).
#
# Output Format: Return only TRUE or FALSE (No additional explanations).
# """
#
# # Configure Google Gemini AI
# genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# model = genai.GenerativeModel('gemini-2.0-flash')
#
# @app.route('/', methods=['GET'])
# def index():
#     return render_template('index.html')
#
# @app.route('/analyze', methods=['POST'])
# def analyze_image():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image uploaded'}), 400
#
#     file = request.files['image']
#     if file.filename == '':
#         return jsonify({'error': 'No image selected'}), 400
#
#     try:
#         # Read and process the image
#         image_bytes = file.read()
#         image = Image.open(io.BytesIO(image_bytes))
#
#         # Generate response from Gemini
#         response = model.generate_content([f"{prompt}", image])
#
#         return jsonify({'description': response.text})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

import os
import io
import time

import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from Alert.notify import alert

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Google Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

# Define the prompt for the AI model
prompt = """
Role: You are a vigilant security guard responsible for monitoring a parking lot.

Task: Analyze the given parking lot image based on the following rules:
1. Proper Parking: Each car must be fully within the boundaries of a single parking space.
2. Line Crossing: Minor overlap of parking lines is acceptable, but excessive crossing that obstructs adjacent spaces is not.
3. Space Conflict: No two cars should be parked in the same designated parking spot.

Analysis Flow:
1. First, identify and analyze the parking lines carefully.
2. Then, determine whether each car is parked correctly based on the rules above.

Response:
1. Return FALSE if all cars comply with the rules (No major action needed).
2. Return TRUE if any rule is significantly violated (Major action needed).

Output Format: Return only TRUE or FALSE (No additional explanations).
"""


def preprocess_image(image_bytes):
    """Applies CLAHE preprocessing to enhance image contrast."""
    image = Image.open(io.BytesIO(image_bytes)).convert('L')  # Convert to grayscale
    img_np = np.array(image)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    processed_img = clahe.apply(img_np)

    # Convert back to PIL Image for compatibility
    processed_pil = Image.fromarray(processed_img)

    # Save the processed image for reference
    processed_pil.save("static/processed_image.jpg")

    return processed_pil


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        # Read and preprocess the image
        image_bytes = file.read()
        processed_image = preprocess_image(image_bytes)

        # Generate response from Gemini
        response = model.generate_content([f"{prompt}", processed_image])
        # print(type(response.text))
        # print(response.text)

        if response.text.strip().upper() == "TRUE":
            print("Sending Message")
            alert("Improper parking detected")

        return jsonify({'description': response.text, 'processed_image': 'static/processed_image.jpg'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
