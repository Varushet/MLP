import streamlit as st
import base64
import os

# Función para convertir imagen local a Base64
def get_image_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.set_page_config(page_title="Mi Proyecto Climático", layout="wide")

image_path = "img/dawn.jpeg"

img_base64 = get_image_as_base64(image_path)

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
    background-color: rgba(255, 255, 255, 0.3);
}}

</style>

<h1>Temperature tool</h1>


""", unsafe_allow_html=True)


paises = [
    'Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
    'Bahamas', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Benin', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burma', 'Burundi',
    'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Congo', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
    'Denmark', 'Djibouti', 'Dominican Republic',
    'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia',
    'Finland', 'France',
    'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
    'Haiti', 'Honduras', 'Hong Kong', 'Hungary',
    'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy',
    'Jamaica', 'Japan', 'Jordan',
    'Kazakhstan', 'Kenya',
    'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania',
    'Madagascar', 'Macedonia', 'Malawi', 'Malaysia', 'Mali', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique',
    'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway',
    'Oman',
    'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
    'Qatar',
    'Reunion', 'Romania', 'Russia', 'Rwanda',
    'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Swaziland', 'Syria',
    'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tunisia', 'Turkey', 'Turkmenistan',
    'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'USA', 'Uruguay', 'Uzbekistan',
    'Venezuela', 'Vietnam',
    'Yemen',
    'Zambia', 'Zimbabwe'
]

# El selector
pais = st.selectbox("🌍 Filtrar por país:", paises)

if pais != "Todos":
    st.success(f"Mostrando datos para: {pais}")
else:
    st.info("Mostrando datos globales")