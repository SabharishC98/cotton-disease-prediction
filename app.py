from flask import Flask, request, render_template, redirect, url_for
import os
import numpy as np
import sqlite3
from keras.preprocessing import image
from keras.applications.resnet50 import ResNet50, preprocess_input

# Initialize Flask app
app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Directory for Kaggle dataset images (Assuming images are organized in folders by disease name)
KAGGLE_DATASET_FOLDER = 'kaggle_dataset'
kaggle_features = {}

# Preventive measures and YouTube links dictionaries
preventive_measures = {
    "Bacterial Blight": ["Use resistant crop varieties.",
    "Implement crop rotation to break the bacteria's lifecycle.",
    "Practice good field hygiene by removing and destroying infected plant debris.",
    "Avoid overhead irrigation to reduce moisture, which promotes bacterial growth.",
    "Apply appropriate bactericides if necessary, following integrated pest management principles."],
    "Alternaria leaf spot": ["Use resistant varieties.",
    "Rotate crops to reduce soil-borne spores.",
    "Remove plant debris to eliminate sources of infection.",
    "Avoid overhead watering to keep leaves dry.",
    "Apply fungicides when necessary, following integrated pest management guidelines.",
    "Ensure proper spacing to improve air circulation and reduce humidity."],
    "Furasium Wilt": ["Use resistant varieties.","Rotate crops with non-host plants.","Improve soil drainage to prevent waterlogging.","Maintain soil health with organic matter.","Avoid planting in infected soil.","Sterilize tools and equipment to prevent spreading the pathogen."],
    "Leaf Curl":["Use resistant plant varieties.","Apply dormant fungicides before bud break.","Remove and destroy infected leaves.","Ensure proper spacing and pruning for good air circulation.","Maintain plant health with appropriate watering and fertilization.","Control insect vectors that may spread the disease."],
    "Verticillium Wilt":["Use resistant varieties.","Rotate crops with non-host plants.","Solarize soil to kill pathogens.","Remove infected plants to stop spread.","Improve soil health with organic matter and good drainage.","Avoid moving contaminated soil."],
    "Cercospora Leaf Spot":["Plant resistant varieties.","Rotate crops to reduce pathogen buildup.","Remove and destroy infected plant debris.","Avoid overhead irrigation to keep foliage dry.","Apply fungicides as part of an integrated pest management plan.","Ensure proper plant spacing to improve air circulation."],
    "disease not identified": ["No preventive measures available"]
}
youtube_links = {"Bacterial Blight":"https://www.youtube.com/embed/_FksFnr7Ug4?si=ItETy-1rJl7tm88q",
       "Alternaria leaf spot":"https://www.youtube.com/embed/f05euNP9vxI?si=Tah1DNvOpsDdkCTI",
       "Furasium Wilt":"https://www.youtube.com/embed/rBVqdVln6G8?si=TvBWB5NVryE2j2WR",
       "Leaf Curl":"https://www.youtube.com/embed/OROpwgKHT2c?si=0WOCyK__zAr4K2BH",
       "Verticillium Wilt":"https://www.youtube.com/embed/hgiatA52nNw?si=zK7Wuslm-favBnZc",
       "Cercospora Leaf Spot":"https://www.youtube.com/embed/vrCJSqFbPik?si=-NUv3f3lxtevkcmy",
       "Disease not identified":None}

# Initialize ResNet50 model
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = model.predict(img_data)
    return features.flatten()

# Precompute features for Kaggle dataset images
def precompute_kaggle_features():
    for root, dirs, files in os.walk(KAGGLE_DATASET_FOLDER):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                img_path = os.path.join(root, file)
                features = extract_features(img_path)
                disease_name = os.path.basename(root)
                kaggle_features[img_path] = (features, disease_name)

def find_similar_image(input_image_path):
    input_features = extract_features(input_image_path)
    conn = sqlite3.connect('image_db.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, features FROM images')
    db_min_dist = float('inf')
    db_closest_name = None

    for name, features_blob in cursor.fetchall():
        db_features = np.frombuffer(features_blob, dtype=np.float32)
        dist = np.linalg.norm(input_features - db_features)
        if dist < db_min_dist:
            db_min_dist = dist
            db_closest_name = name

    conn.close()

    kaggle_min_dist = float('inf')
    kaggle_closest_name = None
    kaggle_closest_path = None

    for img_path, (features, disease_name) in kaggle_features.items():
        dist = np.linalg.norm(input_features - features)
        if dist < kaggle_min_dist:
            kaggle_min_dist = dist
            kaggle_closest_name = disease_name
            kaggle_closest_path = img_path

    if db_min_dist < kaggle_min_dist:
        return db_closest_name, 'database'
    else:
        return kaggle_closest_name, os.path.dirname(kaggle_closest_path)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['image']
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        name, source = find_similar_image(file_path)
        os.remove(file_path)
        return redirect(url_for('prediction', name=name, source=source))
    return render_template('upload.html')

@app.route('/prediction')
def prediction():
    name = request.args.get('name')
    source = request.args.get('source')
    preventive = preventive_measures.get(name, "No preventive measures available.")
    youtube_link = youtube_links.get(name, None)
    return render_template('prediction.html', name=name, source=source, preventive=preventive, youtube_link=youtube_link)

if __name__ == '__main__':
    precompute_kaggle_features()
    app.run(debug=True)
