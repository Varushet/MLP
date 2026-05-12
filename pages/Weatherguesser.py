import streamlit as st
import pandas as pd
import streamlit as st
import base64
import os

# Función para convertir imagen local a Base64
def get_image_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.set_page_config(page_title="Mi Proyecto Climático", layout="wide")

image_path = "img/night.jpeg"

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

<h1>A meteorology based game</h1>

<p>Match an AI to guess a country in the entire world based only on geographic and climatologic data.</p>

""", unsafe_allow_html=True)

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# --- 1. CARGA DE RECURSOS (Solo se ejecuta una vez gracias a cache) ---
@st.cache_resource
def cargar_recursos_juego():
    # SIMULACIÓN DE DATOS Y MODELOS
    data = {
        'Pais': ['España', 'Francia', 'Alemania', 'Italia', 'Reino Unido'],
        'Precipitacion': [600, 700, 800, 900, 1200],      
        'Temp_Media': [13, 11, 9, 14, 10],                
        'Humedad': [65, 75, 78, 70, 82],                  
        'Horas_Sol': [2500, 1800, 1600, 2200, 1400],      
        'Altitud_Media': [600, 300, 200, 400, 150]        
    }
    df = pd.DataFrame(data)
    
    le = LabelEncoder()
    df['Pais_ID'] = le.fit_transform(df['Pais'])
    
    models_list = []
    features_names = [
        ['Precipitacion'],
        ['Precipitacion', 'Temp_Media'],
        ['Precipitacion', 'Temp_Media', 'Humedad'],
        ['Precipitacion', 'Temp_Media', 'Humedad', 'Horas_Sol'],
        ['Precipitacion', 'Temp_Media', 'Humedad', 'Horas_Sol', 'Altitud_Media']
    ]
    
    for feats in features_names:
        X = df[feats]
        y = df['Pais_ID']
        mdl = RandomForestClassifier(n_estimators=10, random_state=42)
        mdl.fit(X, y)
        models_list.append(mdl)
        
    return df, models_list, le, features_names

# Cargamos los recursos
df_juego, lista_modelos, label_encoder, lista_features = cargar_recursos_juego()

# --- 2. INICIALIZACIÓN SEGURA DEL ESTADO ---
# Esto debe estar SIEMPRE al principio para no sobrescribir el estado si ya existe
if 'juego_activo' not in st.session_state:
    st.session_state.juego_activo = False
    st.session_state.intentos = 0
    st.session_state.pais_secreto_obj = None
    st.session_state.historial = []

# --- 3. FUNCIONES ---

def iniciar_juego():
    st.session_state.pais_secreto_obj = df_juego.sample(1).iloc[0]
    st.session_state.intentos = 0
    st.session_state.juego_activo = True
    st.session_state.historial = ["🎮 ¡Partida iniciada! Buena suerte."]
    # No usamos rerun aquí para evitar parpadeos, dejamos que el script continúe

def jugar_turno(guess_jugador):
    if not st.session_state.juego_activo:
        return

    intentos_actuales = st.session_state.intentos
    pais_real_nombre = st.session_state.pais_secreto_obj['Pais']
    
    # 1. Evaluar Jugador
    if guess_jugador.strip().lower() == pais_real_nombre.lower():
        st.session_state.historial.append(f"✅ ¡GANASTE! Adivinaste {pais_real_nombre} en el intento {intentos_actuales + 1}.")
        st.session_state.juego_activo = False
        st.rerun() # Aquí sí recargamos para mostrar pantalla final
        return

    # 2. Evaluar Máquina
    if intentos_actuales < 5:
        modelo_actual = lista_modelos[intentos_actuales]
        features_actuales = lista_features[intentos_actuales]
        
        datos_input = st.session_state.pais_secreto_obj[features_actuales].values.reshape(1, -1)
        prediccion_id = modelo_actual.predict(datos_input)[0]
        pais_predicho_maquina = label_encoder.inverse_transform([prediccion_id])[0]
        
        msg_maquina = f"🤖 **Turno {intentos_actuales + 1}:** La máquina apuesta por {pais_predicho_maquina}."
        
        if pais_predicho_maquina == pais_real_nombre:
            st.session_state.historial.append(msg_maquina + " 🏆 ¡La máquina ha ganado!")
            st.session_state.juego_activo = False
        else:
            st.session_state.historial.append(msg_maquina + " ❌ Falló.")
            st.session_state.intentos += 1
            
            if st.session_state.intentos >= 5:
                st.session_state.historial.append(f"💀 Fin del juego. Era {pais_real_nombre}.")
                st.session_state.juego_activo = False
            else:
                st.session_state.historial.append(f"⏳ Siguiente ronda...")
                
    st.rerun()

# --- 4. INTERFAZ (UI) ---

st.title("🌍 Duelo Climático: Humano vs IA Progresiva")

# DEBUG: Para ver si el estado se mantiene (puedes borrar esto luego)
# st.caption(f"DEBUG: juego_activo = {st.session_state.juego_activo}, intentos = {st.session_state.intentos}")

if not st.session_state.juego_activo:
    st.info("La máquina empieza 'ciega' y va aprendiendo cada turno.")
    if st.button("🚀 Empezar Reto", key="btn_start"):
        iniciar_juego()
        st.rerun() # Forzamos recarga inmediata para entrar en el modo juego

else:
    # Estamos EN JUEGO
    num_vars = len(lista_features[st.session_state.intentos])
    st.markdown(f"### Ronda {st.session_state.intentos + 1}/5")
    st.caption(f"La máquina usa **{num_vars} variable(s)** climática(s).")
    
    # Pista pública (siempre mostramos la primera variable como pista básica)
    primera_var = lista_features[0][0]
    valor_pista = st.session_state.pais_secreto_obj[primera_var]
    st.metric(label=f"Pista: {primera_var}", value=valor_pista)

    # Input y Botón
    col1, col2 = st.columns([3, 1])
    with col1:
        guess = st.text_input("Tu predicción:", key="guess_input", placeholder="Escribe el país...")
    with col2:
        # El botón debe tener una key única si hay varios botones
        if st.button("Enviar", key="btn_send"):
            if guess:
                jugar_turno(guess)
            else:
                st.error("Escribe un nombre.")

    st.markdown("---")
    st.subheader("Historial:")
    for h in st.session_state.historial:
        st.write(h)