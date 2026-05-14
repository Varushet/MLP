import streamlit as st
import base64
import os

st.set_page_config(page_title="Mi Proyecto Climático", layout="wide")

# Función para convertir imagen local a Base64
def get_image_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Ruta de tu imagen
image_path = "img/day.jpg"

# Generar la cadena base64
img_base64 = get_image_as_base64(image_path)

# NOTA LA 'f' ANTES DE LAS COMILLAS TRIPLES -> f"""
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}}
.stApp h1 {{
    color: rgba(255, 255, 255);
    font-size: 5rem; 
    font-weight: bold;
    padding: 1rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}
.stApp p {{
    color: rgba(255, 255, 255);
    margin: 3rem 0;
    font-size: 2rem; 
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}
[data-testid="stSidebar"] {{
    background: rgba(100, 100, 100, 0.7) !important;
}}

</style>

<h1>Bienvenido a Weathery</h1>

<p>Un proyecto de Machine Learning sobre el clima del planeta</p>
<p>Explora las diferentes herramientas y funcionalidades creadas a partir de fuentes de datos y sus predicciones:</p>

""", unsafe_allow_html=True)