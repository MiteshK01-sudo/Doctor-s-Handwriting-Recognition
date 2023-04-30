import smtplib
from flask import Flask, request, render_template, jsonify
import io
import os
from google.cloud import vision_v1, vision
from google.cloud.vision_v1 import types
import openai
from google.oauth2 import service_account
openai.api_key = "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"


# Set up Google Cloud Vision API client
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "ServiceAccountToken.json"
#client = vision_v1.ImageAnnotatorClient()


#import os
#from google.cloud import vision_v1


# Set up Google Cloud Vision API client with credentials
credentials = service_account.Credentials.from_service_account_info({
    "type": "service_account",
    "project_id": "hardy-force-380207",
    "private_key_id": "01fc9250f8973040209a2c384e63866776360d61",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC9iLV1W5mrDAMX\nV6nF4VcSC6oplxwHzLnWFpZj+N8HCPMUnl2UAWWIK7kvCT1cGWrYGPnZNoVvkv/c\nHJpJhoBDOTLIGJ6EQqRvaCxlpucW7S9a9OdWfsxeaBoR36hp6EU5QTBgMjqug3Yc\n5JspieBfnHzo1rOx02WR8day3hvxGCiOY4I4LLmrQJuG/whDIC3oYTY4C3FIna06\nos1zdGKBFi6DUmouzDHPhte5oZlWTgQJ3TtYi8FNhL3pTXCcoMeO3wdZCFaJvuy7\nmFS/0Q7geHUOzuQNcRFfFPcoG7djStGJvsYMqMKmpQaSSiAQpqtqmmpd8bpLr1s4\neNrSsfILAgMBAAECggEAFVxE5xcNuINADe9pSM3enEAIS2umUxK1lvUwuc+ggxB1\nJMu8TCPkJ3aWBkEKU0jiC7y029ATNcHhaBMpKEQqTGkz2e08YDeKhKu+5S3sOV89\nyQh00gC0U6dz2LPWLSlqM8uvAghnKKfUNellu0a4rM3cHfmkgtQKTGpvAfWaPI+E\njLxbB6A7xL2z+3uBmuBkKGVv05gv9d+2rydqq/2moxAy4L7TYagjLUAtuyMaxJ5c\nI+3O6QPMUfFh4Cn+J3J5PwEdgtVgRw2TUm8+SUPKUDWByrViv2EZGDARVHrSKUVF\nloTCpOF3dKswR2VkoPULxH6XoqGemiJ7+SgVibNe0QKBgQDzZDR+ZwJNijdgw6T7\neq5V+yN5/l9GMLygX20qKD38sYSGBSvq77wDCU+zda8pOFmpc2L22TmrrdLdAb/Z\n79VUctULEnnRsXq7GLMuxRbspCMtZpE7iKcipFZmzR9llcCokZJWpOFDXrmVcKw4\nN8oAWGv7RRs5t/3gNFknhbrpTQKBgQDHWkK1w1PCHy7GrgTRSvmbLMCsdC2slN/9\ntuHV6w3S07MA1+40XRh45iAGIoFy9/9HuQA8FMAwLraHfzsEW/IJe8IDWRqTqhqo\nc3XdPqiKflUSaWVUD12RhLQc/MYofBuiN8wtogEo+PEGJleLblPxhDNrqG0XtCq3\n0o7L/HPctwKBgQDjelAlo5jfZ8MCSVi1QaAW9DXgGwJo07w4F3gr4pisyC0YJVU6\nqv2JyPYYwHEJkYUbfqCMHdJsxnVB4hSxWBqGZxz+0DHS7pHKs/ckS0h1u6K1GBu9\nDKdJFVc7lZM2mpQJ+KRRHqD7GllRdpE/qcS+NeYWXixn8bLyDXsWGULsMQKBgQCw\np4hz/3oKjI1r3CtCt/jGjHrUl0MeKvLuppAre1bNm3GFbtOULWcRQ4PfS9aAZcke\n6o6Nrym7yLlRCurmav/pbXS4eM43SkbDPUWV3/+Ecny6ixES02bsG7dr9Ic4uvnV\n3zIcwfHbN/aFp5ZuZT8Xxzm1zhOWLL6qFHkbxEN7swKBgDTQalnomKIIZGRtr24D\n9UNja435WDf5lPwI/Wycu59a95fmr/0ZpWy3zlx05zJPXnhBwCCL/4qatja9z2Gs\nqvv/A6m/gH1/BiKcqptPz3Qup3RDxJaO6YLm5Zgaw3G15JUmobpxwrgWDyQDf2//\nTf5rfVHjxWR9KTzjG53tOddP\n-----END PRIVATE KEY-----\n",
    "client_email": "visionapi-service-account@hardy-force-380207.iam.gserviceaccount.com",
    "client_id": "111898539038421184006",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/visionapi-service-account%40hardy-force-380207.iam.gserviceaccount.com"
})

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = None

client = vision_v1.ImageAnnotatorClient(credentials=credentials)





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
