import smtplib
from flask import Flask, request, render_template, jsonify
import io
import os
from google.cloud import vision_v1, vision
from google.cloud.vision_v1 import types
import openai
openai.api_key = "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"


# Set up Google Cloud Vision API client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceAccountToken.json'
client = vision_v1.ImageAnnotatorClient()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze_image', methods=['POST'])
def analyze_image():
    # Get the image from the request
    file = request.files['image']
    content = file.read()

    # Call the Google Cloud Vision API to analyze the image
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text

    # Return the result as JSON
    return jsonify({'text': text})

@app.route('/api/suggest_remedies', methods=['POST'])
def suggest_remedies():
    input_text = request.form["feeling"]

    # Generate response using OpenAI GPT-3 API
    model_engine = "text-davinci-002"
    prompt = f"What can I do to feel better if I'm {input_text}?"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )
    suggestions = completions.choices[0].text.strip()
    return jsonify({'suggestions': suggestions})
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    to = 'your_mail'
    subject = 'New message from website'
    body = f'Name: {name}\nEmail: {email}\nMessage:\n{message}'

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_mail', 'password')
        server.sendmail('your_email@gmail.com', to, body)
        server.quit()
        return 'Email sent successfully!'
    except:
        return 'Error sending email'

if __name__ == '__main__':
    app.run()
