from dotenv import load_dotenv
import json
import os
import requests
from datetime import date
load_dotenv()

from flask import Flask, send_file, render_template, url_for, Response
app = Flask(__name__, template_folder='templates')

# Delete all images not from today
def clear_images():
    today = date.today().strftime("%Y-%m-%d")
    for file in os.listdir('images'):
        if file != f'{today}.jpg':
            os.remove(f'images/{file}')

"""
Displays the COTD from the NASA API
"""
@app.route('/')
def main():
    clear_images()
    # Get the date
    today = date.today().strftime("%Y-%m-%d")
    # Check if we have an image for the day already
    # Images are stored in the images folder and have the format YYYY-MM-DD.jpg
    if not os.path.isfile(f'images/{today}.jpg'):
        # If we don't have an image, get it from the NASA API
        # Get the API key from the .env file
        api_key = os.getenv('API_KEY')
        # Get the COTD from the NASA API
        response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}')
        # Parse the response
        data = json.loads(response.text)
        # Get the image URL
        image_url = data['url']
        # Get the image
        image = requests.get(image_url)
        # Save the image
        with open(f'images/{today}.jpg', 'wb') as f:
            f.write(image.content)
    
    # Return the image
    return render_template('index.html', image=f'images/{today}.jpg')

@app.route('/image')
def image():
    today = date.today().strftime("%Y-%m-%d")
    
    def generate():
        with open(f'images/{today}.jpg', 'rb') as f:
            while True:
                data = f.read()
                if not data:
                    break
                yield data
    return Response(generate(), content_type='image/jpeg')


if __name__ == '__main__':
    app.run()
