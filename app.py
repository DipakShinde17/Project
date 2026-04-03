# import streamlit as st
# import tensorflow as tf
# import numpy as np
# from PIL import Image

# # Load your trained model
# model = tf.keras.models.load_model("model.h5")

# # Class names (change according to your dataset)
# class_names = ["Wheat", "Rice", "Maize", "Cotton"]  

# st.title("🌾 Agricultural Crop Classification")
# st.write("Upload a crop image to predict the category")

# uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_column_width=True)

#     img = image.resize((64, 64))  # use your training size
#     img = np.array(img) / 255.0
#     img = np.expand_dims(img, axis=0)

#     prediction = model.predict(img)
#     predicted_class = class_names[np.argmax(prediction)]

#     st.success(f"Prediction: {predicted_class}")

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load model
model = tf.keras.models.load_model("model.h5")

# 🔥 UPDATE THIS LIST ACCORDING TO YOUR DATASET
class_names = [
    "Cherry",
    "Coffee-plant",
    "Cucumber",
    "Fox_nut(Makhana)",
    "Lemon",
    "Olive-tree",
    "Pearl_millet(bajra)",
    "Tobacco-plant",
    "almond",
    "banana",
    "cardamom",
    "chilli",
    "clove",
    "coconut",
    "cotton",
    "gram",
    "jowar",
    "jute",
    "maize",
    "mustard-oil",
    "papaya",
    "pineapple",
    "rice",
    "soyabean",
    "sugarcane",
    "sunflower",
    "tea",
    "tomato",
    "vigna-radiati(Mung)",
    "wheat"
]


st.title("🌾 Agricultural Crop Classification")
st.write("Upload a crop image to predict the category")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image")

    img = image.resize((64, 64))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    predicted_index = np.argmax(prediction)

    # Extra safety check
    if predicted_index < len(class_names):
        predicted_class = class_names[predicted_index]
        st.success(f"Prediction: {predicted_class}")
    else:
        st.error("Class index mismatch. Please check class_names list.")
