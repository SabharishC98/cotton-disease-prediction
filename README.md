# 🌿 Cotton Leaf Disease Prediction Website

This project is a web-based application that predicts cotton leaf diseases using image classification with a trained deep learning model.

The system uses a Convolutional Neural Network (CNN) to analyze cotton leaf images uploaded by users and determines which disease affects the plant.

---

## 📌 Features

- Upload cotton leaf image for prediction
- Deep learning based disease detection
- Simple and user-friendly web interface
- Built using Python, Flask, and TensorFlow/Keras

---

## 🛠️ Technologies Used

- Python
- TensorFlow / Keras
- Flask
- HTML, CSS
- OpenCV
- Numpy
- VS Code

---

---

## 🚀 How To Run This Project

### Step 1: Install Required Libraries

Open terminal or VS Code terminal and run:

```bash
pip install -r requirements.txt
Step 2: Run image_db.py (Important First Step)
Before running the web application, you must execute:

bash
Copy code
python image_db.py
✅ This will prepare the image database / load the model / setup required resources for the prediction system.

⚠️ Without running this file first, the system may not work properly.

Step 3: Run the Flask Web App
After image_db.py runs successfully, start the website:

bash
Copy code
python app.py
Now open your browser and go to:

👉 http://127.0.0.1:5000/

Upload a cotton leaf image and get the prediction result.

🧠 Supported Cotton Diseases
Bacterial Blight

Curl Virus

Fusarium Wilt

Healthy Leaf

📥 Dataset
Dataset consists of cotton leaf images categorized by disease:

Healthy

Bacterial Leaf Blight

Leaf Curl Disease

Leaf Spot

Dataset is organized into training and validation folders.


👨‍💻 Author
Sabharish C
Dr. N.G.P Institute of Technology