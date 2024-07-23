# Gym-classifier
The Gym Classifier is a web application that allows users to upload images of gym equipment, which are then classified using OpenAI's GPT-4 model. The application provides the name of the gym equipment, a description of how to use it, the muscles it targets, and common tips or mistakes to avoid. Additionally, the app provides a link to a short YouTube tutorial video related to the equipment.

## Features
- Upload images of gym equipment.
- Automatically classify and describe the gym equipment using OpenAI's GPT-4 model.
- Provide a YouTube tutorial video link for using the equipment.
- Supports cross-origin requests using Flask-CORS.

## To use normally
Simply click on the link to the github page. 
here is the link: https://matthewkweon.github.io/Gym-classifier/ 

## To edit the code and use in your own context
Prerequisites
- Python 3.8 or higher
- Git
- Heroku CLI

### Install Dependencies

```
pip install -r requirements.txt
```


### Set Up Environment Variables
Create a .env file in the root directory and add your OpenAI API key and YouTube API key:

```
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
```
You can create your own api's using openAI and youtube's websites and softwares.

### Run the Application Locally

```
python app.py
```

### Deploy to Heroku
Log in to Heroku:

```
heroku login
```
Create a new Heroku app:


```
heroku create gym-classifier
```
Set the buildpacks for the app:
```
heroku buildpacks:add heroku/python
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
```
Create an Aptfile in the root directory with the following content:


```
libgl1-mesa-glx
libglib2.0-0
```

Add your environment variables to Heroku:

```
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set YOUTUBE_API_KEY=your_youtube_api_key
```
Deploy the app:

```
git add .
git commit -m "Deploying Gym Classifier"
git push heroku main
```

### Access the Application
Open your browser and navigate to the URL provided by Heroku (e.g., https://gym-classifier.herokuapp.com).

### Usage
- Open the web application.
- Upload an image of the gym equipment.
- Click the "Submit" button.
- The application will display the name of the gym equipment, a description, and a link to a YouTube tutorial video.

## Dependencies
Dependencies
Flask
Flask-CORS
OpenAI
Pillow
Requests
Gunicorn
OpenCV


## Acknowledgments
OpenAI for providing the GPT-4 model.
YouTube Data API for providing video tutorials.

