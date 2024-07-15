import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from openai import OpenAI
from PIL import Image
import base64
import io
import requests
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://matthewkweon.github.io"}})

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = OpenAI()

# Include the functions from your original code
def encode_image(image_path):
    with Image.open(image_path) as img:
        img.thumbnail((1024, 1024))
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

def parse_duration(duration):
    match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
    if not match:
        return 0
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds

def search_youtube(query):
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        return "YouTube API key not found"

    search_url = "https://www.googleapis.com/youtube/v3/search"
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    
    search_params = {
        'part': 'snippet',
        'q': f"{query} tutorial",
        'key': api_key,
        'maxResults': 50,
        'type': 'video'
    }
    
    try:
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        tutorial_videos = [
            item for item in search_data.get('items', [])
            if 'tutorial' in item['snippet']['title'].lower()
        ]
        
        for video in tutorial_videos:
            video_id = video['id']['videoId']
            video_params = {
                'part': 'contentDetails',
                'id': video_id,
                'key': api_key
            }
            
            video_response = requests.get(video_url, params=video_params)
            video_response.raise_for_status()
            video_data = video_response.json()
            
            duration = video_data['items'][0]['contentDetails']['duration']
            duration_seconds = parse_duration(duration)
            
            if duration_seconds <= 180:
                return f"https://www.youtube.com/watch?v={video_id}"
        
        return f"No suitable tutorial videos found for query: {query}"
    
    except requests.RequestException as e:
        return f"Error fetching YouTube data: {str(e)}"

def extract_equipment_name(description):
    equipment_match = re.search(r"Equipment: (.+?)\.?(\n|$)", description)
    if equipment_match:
        return equipment_match.group(1).strip()
    
    first_sentence = description.split('.')[0]
    noun_phrase_match = re.search(r"(The|A|An) (.+)", first_sentence, re.IGNORECASE)
    if noun_phrase_match:
        return noun_phrase_match.group(2).strip()
    
    words = description.split()
    return ' '.join(words[:3]) if len(words) > 3 else ' '.join(words)

def classify_gym_equipment(image_path):
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Identify the gym equipment shown in this image. Please provide the name of the gym equipment as so: ''Equipment: name of equipment.'' Provide a brief, 3-paragraph description including: 1) What the equipment is, 2) How it's used and what muscles it targets, and 3) Tips for proper form or common mistakes to avoid. Keep each paragraph concise, about 2-3 sentences long."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    description = response.choices[0].message.content
    
    equipment_name = extract_equipment_name(description)
    search_query = f"{equipment_name} gym tutorial"
    video_link = search_youtube(search_query)

    return description, video_link

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        description, video_link = classify_gym_equipment(filepath)

        return jsonify({
            'description': description,
            'video_link': video_link
        })
    
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

"""gpt: sk-proj-sXORIZbmRQZuwh4LPkv3T3BlbkFJXw2IVGh1JH8igaY1KnuR"""
"""Youtube: AIzaSyBNjJ77RFoRtdIyB9UtoAfTOKMfMPZbdAw"""