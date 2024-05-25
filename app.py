from flask import Flask, render_template, request, redirect, url_for
from flask import session
from pymongo import MongoClient
import requests
# MongoDB-ga bog'lanish
client = MongoClient('mongodb://localhost:27017/')
db = client['testdb']
collection = db['user']
users = collection.find()




app = Flask(__name__)

from flask import send_from_directory

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)


# home
@app.route('/')
def index():
    return render_template('index.html')


# Admin sahifasi (faqatgina "admin" foydalanuvchi kirganida)
@app.route('/admin')
def admin():
    if 'username' in session: 
        # Foydalanuvchilarni MongoDB-dan olish
        users = collection.find()
        return render_template('admin.html', username=session['username'], users=users)
    return redirect(url_for('login'))


# Foydalanuvchi profili sahifasi
@app.route('/profile')
def profile():
    username = session.get('username')
    if not username or username == "admin":
        return redirect(url_for('login'))
    
    user = collection.find_one({'username': username})
    
    return render_template('profile.html', user=user)


# Autentifikatsiya
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == "admin" and password == "admin":
            session['username'] = username
            return redirect(url_for('admin'))
        
        user = collection.find_one({'username': username})
        
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('profile'))
        
        return render_template('login.html', error_message='Foydalanuvchi nomi yoki parol noto`g`ri kiritildi!!!')
    
    return render_template('login.html')



#registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = collection.find_one({'username': username})
        if user:
            return render_template('register.html', error_message='Bu foydalanuvchi nomi allaqachon mavjud')
        
        collection.insert_one({'username': username, 'password': password})
        # Foydalanuvchilarni MongoDB-dan olish
        users = collection.find()
        return redirect(url_for('admin', users=users))
    
    return render_template('register.html')

@app.route('/price')
def price():
    return render_template('price.html')

@app.route('/shares')
def shares():
    return render_template('shares.html')

@app.route('/collaboration')
def collaboration():
    return render_template('collaboration.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

#huggingfase speech to text
import requests
stt_API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
stt_headers = {"Authorization": "Bearer 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"}

from werkzeug.utils import secure_filename

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(filename)
    return 'File uploaded successfully!'


@app.route('/stt', methods=['GET', 'POST'])
def stt():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(filename)
        response = query(filename)
        return response['text']
    if request.method == 'POST':
        audio_data = request.form['audio_data']
        response = query(audio_data)
        return response['text']
    return render_template('stt.html')

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(stt_API_URL, headers=stt_headers, data=data)
    return response.json()

#huggingfase image classificaton

imageClas_API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
imageClas_headers = {"Authorization": "Bearer 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"}

@app.route('/imageClas', methods=['GET', 'POST'])
def imageClas():
    if request.method == 'POST':
        # Handle POST request
        pass
    return render_template('imageClas.html') 

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(imageClas_API_URL, headers=imageClas_headers, data=data)
    return response.json()

#huggingfase image segmentation

imageSeg_API_URL = "https://api-inference.huggingface.co/models/facebook/mask2former-swin-large-cityscapes-semantic"
imageSeg_headers = {"Authorization": "Bearer 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"}

@app.route('/imageSeg', methods=['GET', 'POST'])
def imageSeg():
    if request.method == 'POST':
        # Handle POST request
        pass
    return render_template('imageSeg.html')

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(imageSeg_API_URL, headers=imageSeg_headers, data=data)
    return response.json()

#huggingfase text to image

textImage_API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
textImage_headers = {"Authorization": "Bearer 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"}

@app.route('/textImage', methods=['GET', 'POST'])
def textImage():
    if request.method == 'POST':
        # Handle POST request
        pass
    return render_template('textImage.html')

def query(payload):
	response = requests.post(textImage_API_URL, headers=textImage_headers, json=payload)
	return response.content
image_bytes = query({
	"inputs": "Astronaut riding a horse",
})
# You can access the image with PIL.Image for example
import io
from PIL import Image
image = Image.open(io.BytesIO(image_bytes))

#huggingfase image to text

imageText_API_URL = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
imageText_headers = {"Authorization": "Bearer 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"}

@app.route('/imageText', methods=['GET', 'POST'])
def imageText():
    if request.method == 'POST':
        # Handle POST request
        pass
    return render_template('imageText.html')

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(imageText_API_URL, headers=imageText_headers, data=data)
    return response.json()




#huggingfase  text to speech
from transformers import AutoModel, AutoTokenizer
import torch



model = AutoModel.from_pretrained("facebook/mms-tts-uzb-script_cyrillic")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-uzb-script_cyrillic")

text = "some example text in the Uzbek language"
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    output = model(**inputs).waveform

import scipy

scipy.io.wavfile.write("techno.wav", rate=model.config.sampling_rate, data=output)

from IPython.display import Audio

Audio(output, rate=model.config.sampling_rate)

# textSpeech_API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-uzb-script_cyrillic"
# textSpeech_headers = {"Authorization": "Bearer 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"}

# @app.route('/textSpeech', methods=['GET', 'POST'])
# def textSpeech():
#     if request.method == 'POST':
#         # Handle POST request
#         pass
#     return render_template('textSpeech.html')

# def query(payload):
# 	response = requests.post(textSpeech_API_URL, headers=textSpeech_headers, json=payload)
# 	return response.content

# audio_bytes = query({
# 	"inputs": "The answer to the universe is 42",
# })
# # You can access the audio with IPython.display for example
# from IPython.display import Audio
# Audio(audio_bytes)




# Chiqish (sessiyani tark etish)
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'sirli_kalit'
    app.run()
