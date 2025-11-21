import sqlite3
import numpy as np
from keras.preprocessing import image  
from keras.applications.resnet50 import ResNet50, preprocess_input

# Initialize ResNet50 model
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = model.predict(img_data)
    return features.flatten()

def create_database():
    conn = sqlite3.connect('image_db.sqlite')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS images
                      (id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      features BLOB NOT NULL)''')
    
    # Insert initial data
    images = [
        ('Alternaria leaf spot', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\alternaria1.jpg"),
        ('Alternaria leaf spot', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\alternaria2.jpg"),
        ('Alternaria leaf spot', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\alternaria3.jpg"),
        ('Alternaria leaf spot', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\alternaria4.jpg"),
        ('Bacterial Blight', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\Bacterial1.jpg"),
        ('Bacterial Blight', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\Bacterial2.jpg"),
        ('Bacterial Blight', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\Bacterial3.jpg"),
        ('Bacterial Blight', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\Bacterial4.jpg"),
        ('Furasium Wilt', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\wilt1.jpg"),
        ('Furasium Wilt', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\wilt2.jpg"),
        ('Furasium Wilt', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\wilt3.png"),
        ('Furasium Wilt', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\wilt4.jpg"),
        ('Leaf Curl', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\leaf1.jpg"),
        ('Leaf Curl', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\leaf2.png"),
        ('Leaf Curl', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\leaf3.png"),
        ('Leaf Curl', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\leaf4.jpg"),
        ('Leaf Curl', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\leaf5.jpg"),
        ('Verticillium Wilt', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\vert1.png"),
        ('Verticillium Wilt', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\vert2.jpg"),
        ('Verticillium Wilt', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\vert3.jpg"),
        ('Verticillium Wilt', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\vert4.jpg"),
        ('Verticillium Wilt', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\vert5.jpg"),
        ('Cercospora Leaf Spot', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\cer1.jpg"),
        ('Cercospora Leaf Spot', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\cer2.jpg"),
        ('Cercospora Leaf Spot', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\cer3.jpg"),
        ('Cercospora Leaf Spot', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\cer4.jpg"),
        ('Cercospora Leaf Spot', r"C:\Users\sabha\OneDrive\Documents\GTA Vice City User Files\python_alone\images\cer5.jpg")
    ]
    
    for name, path in images:
        features = extract_features(path)
        cursor.execute('INSERT INTO images (name, features) VALUES (?, ?)', (name, features.tobytes()))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
