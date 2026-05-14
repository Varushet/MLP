import streamlit as st
import pandas as pd
import base64
import joblib
import numpy as np
from collections import Counter

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
    color: #D3D3D3;
    font-size: 4.5rem;
    font-weight: bold;
    padding: 1.2rem 2rem 1.2rem 2rem;
    border-radius: 1.5rem;
    margin-bottom: 2rem;
    text-shadow: 0 2px 8px #C0C0C0CC;
    display: inline-block;
}}
.stApp p, .stApp .stMarkdown p {{
    color: #D3D3D3;
    border-radius: 1rem;
    padding: 1rem 2rem;
    font-size: 1.5rem;
    font-weight: 500;
    margin: 2rem 0;
    text-shadow: 0 2px 8px #C0C0C0CC;
    text-align: center;
    justify-content: center;
}}
.stApp .stDataFrame, .stApp .stTable, .stApp .stAlert, .stApp .stMarkdown, .stApp .stButton, .stApp .stNumberInput, .stApp .stSelectbox {{
    background: #102A43CC !important;
    border-radius: 1.2rem !important;
    box-shadow: 0 2px 16px 0 #C0C0C0CC;
    color: #fff8f0 !important;
    text-align: center;
    justify-content: center;
}}
.stApp button, .stApp .stButton>button {{
    background: linear-gradient(90deg, #102A43 0%, #C0C0C0 100%) !important;
    border: none !important;
    border-radius: 1.2rem !important;
    font-weight: bold !important;
    font-size: 1.2rem !important;
    box-shadow: 0 4px 10px 0 #C0C0C0CC;
    transition: background 0.3s, color 0.3s;
    text-align: center;
}}
.stApp button:hover, .stApp .stButton>button:hover {{
    background: linear-gradient(90deg, #C0C0C0 0%, #102A43 100%) !important;
}}
.stApp input, .stApp select, .stApp textarea {{
    color: rgba(255, 248, 240) !important;
    font-size: 1.1rem !important;
}}
[data-testid="stSidebar"] {{
    color: rgba(0, 0, 0) !important;
    background: rgba(100, 100, 100, 0.7) !important;
    border-radius: 1.5rem 0 0 1.5rem;
    box-shadow: 2px 0 16px 0 rgba(255, 183, 94, 0.10);
}}
::-webkit-scrollbar {{ width: 10px; background: #ffecd0; }}
::-webkit-scrollbar-thumb {{ background: #ffb75e; border-radius: 8px; }}
.stApp .stNumberInput input, .stApp .stSelectbox div {{ color: rgba(255, 234, 208) !important; }}
.stApp .stDataFrame th, .stApp .stDataFrame td {{ background: rgba(255,255,255,0.85) !important; color: #3d2c1e !important; }}
.stApp .stAlert[data-baseweb="notification"] {{
    background: linear-gradient(90deg, #ffecd0 0%, #ffb75e 100%) !important;
    color: #3d2c1e !important;
    border-radius: 1.2rem !important;
}}
</style>

<h1>A meteorology based game</h1>
<p>Match an AI to guess a country in the entire world based only on geographic and climatologic data.</p>
""", unsafe_allow_html=True)


# --- 1. CARGA DE RECURSOS ---

@st.cache_resource
def cargar_recursos_juego():
    df = pd.read_csv('data/climaDS.csv.gz')
    modelo = joblib.load('models/final_boss.pkl')

    col_id   = 'country_id'
    col_name = 'country'

    if col_id not in df.columns or col_name not in df.columns:
        st.error(f"Columnas no encontradas. Revisa que '{col_id}' y '{col_name}' existan en el CSV.")
        st.stop()

    # Orden exacto del entrenamiento — no cambiar
    all_features_model = ['longitude', 'temp_C', 'humidity', 'precip_mm', 'wind_kph', 'cloud', 'Air_poll', 'sun_h']

    # Las features más dominantes (temp_C, longitude) se revelan las últimas
    # para que la IA empiece ciega y converja al final
    features_names = [
        ['precip_mm', 'cloud'],
        ['precip_mm', 'cloud', 'wind_kph'],
        ['precip_mm', 'cloud', 'wind_kph', 'humidity', 'Air_poll'],
        ['precip_mm', 'cloud', 'wind_kph', 'humidity', 'Air_poll', 'sun_h'],
        ['precip_mm', 'cloud', 'wind_kph', 'humidity', 'Air_poll', 'sun_h', 'temp_C'],
        ['precip_mm', 'cloud', 'wind_kph', 'humidity', 'Air_poll', 'sun_h', 'temp_C', 'longitude'],
    ]
    return df, modelo, col_id, col_name, features_names, all_features_model


df_juego, modelo_ia, col_id, col_name, lista_features, all_features_model = cargar_recursos_juego()

# Precalculamos la matriz de features del dataset entero para el sampleo
matriz_dataset = df_juego[all_features_model].values


# --- 2. PREDICCIÓN POR VOTACIÓN CON FILAS REALES ---

def predecir_con_votacion(pais_secreto, features_visibles, n_votos=300):
    """
    Para cada voto, las features ocultas se toman de una fila real aleatoria
    del dataset. Esto garantiza que las combinaciones de valores sean siempre
    climáticamente coherentes (ningún modelo ve temp=45°C + longitud de Siberia).

    Las features reveladas son siempre el valor real del país secreto.
    El país que acumula más votos gana.
    """
    # Samplear n_votos filas reales del dataset (con reemplazo)
    idx_random = np.random.randint(0, len(matriz_dataset), size=n_votos)
    filas_random = matriz_dataset[idx_random]  # shape: (n_votos, n_features)

    # Construir la matriz de inputs: para features visibles, usar el valor real
    inputs = filas_random.copy()
    for i, feat in enumerate(all_features_model):
        if feat in features_visibles:
            inputs[:, i] = pais_secreto[feat]

    predicciones = modelo_ia.predict(inputs)
    return Counter(predicciones.tolist()).most_common(1)[0][0]


# --- 3. INICIALIZACIÓN DEL ESTADO ---

if 'juego_activo' not in st.session_state:
    st.session_state.juego_activo = False
    st.session_state.intentos = 0
    st.session_state.pais_secreto_obj = None
    st.session_state.historial = []


# --- 4. FUNCIONES DE JUEGO ---

def iniciar_juego():
    st.session_state.pais_secreto_obj = df_juego.sample(1).iloc[0]
    st.session_state.intentos = 0
    st.session_state.juego_activo = True
    st.session_state.historial = ["🎮 ¡Partida iniciada! Buena suerte."]


def jugar_turno(guess_jugador):
    if not st.session_state.juego_activo:
        return

    intentos_actuales = st.session_state.intentos
    pais_secreto      = st.session_state.pais_secreto_obj
    pais_real_nombre  = pais_secreto[col_name]
    pais_real_id      = pais_secreto[col_id]

    # 1. Evaluar al jugador
    if guess_jugador.strip().lower() == pais_real_nombre.lower():
        st.session_state.historial.append(
            f"✅ ¡GANASTE! Adivinaste **{pais_real_nombre}** en el intento {intentos_actuales + 1}."
        )
        st.session_state.juego_activo = False
        st.rerun()
        return

    # 2. Features disponibles este turno
    max_pistas        = min(intentos_actuales + 1, len(lista_features))
    features_visibles = lista_features[max_pistas - 1]

    # 3. Predicción por votación con filas reales
    prediccion_id    = predecir_con_votacion(pais_secreto, features_visibles, n_votos=300)
    prediccion_match = df_juego[df_juego[col_id] == int(prediccion_id)]

    pais_predicho_maquina = (
        prediccion_match.iloc[0][col_name]
        if not prediccion_match.empty
        else "Desconocido"
    )

    msg_maquina = f"🤖 **Turno {intentos_actuales + 1}:** La máquina apuesta por **{pais_predicho_maquina}**."

    if int(prediccion_id) == int(pais_real_id):
        st.session_state.historial.append(msg_maquina + " 🏆 ¡La máquina ha acertado!")
    else:
        st.session_state.historial.append(msg_maquina + " ❌ Falló.")

    # 4. Fin de juego
    st.session_state.intentos += 1
    if st.session_state.intentos >= 5:
        st.session_state.historial.append(f"💀 Fin del juego. Era **{pais_real_nombre}**.")
        st.session_state.juego_activo = False
        st.session_state.pais_secreto_final = pais_real_nombre
    else:
        st.session_state.historial.append("⏳ Siguiente ronda...")

    st.rerun()


# --- 5. INTERFAZ (UI) ---

st.title("🌍 Duelo Climático: Humano vs IA Progresiva")

if not st.session_state.juego_activo:
    st.info("La máquina empieza 'ciega' y va aprendiendo cada turno.")
    if st.button("🚀 Empezar Reto", key="btn_start"):
        iniciar_juego()
        st.rerun()
    if 'pais_secreto_final' in st.session_state:
        st.success(f"El país secreto era: {st.session_state.pais_secreto_final}")
        del st.session_state.pais_secreto_final
else:
    max_pistas = min(st.session_state.intentos + 1, len(lista_features))
    num_vars   = len(lista_features[max_pistas - 1])
    st.markdown(f"### Ronda {st.session_state.intentos + 1}/5")
    st.caption(
        f"La máquina usa **{num_vars} variable(s)** climática(s). "
        f"Se revelan: {', '.join(lista_features[max_pistas - 1])}"
    )

    # Mostrar pistas en formato compacto (barra horizontal)
    pistas_html = ""
    for var in lista_features[max_pistas - 1]:
        valor = st.session_state.pais_secreto_obj[var]
        pistas_html += f"<div style='display: inline-block; background: linear-gradient(90deg, #102A43 0%, #C0C0C0 100%); border-radius: 0.8rem; padding: 0.5rem 1rem; margin: 0.3rem; text-align: center; color: #fff8f0; font-weight: bold; font-size: 0.9rem;'><strong>{var}</strong><br><span style='font-size: 1.1rem;'>{valor}</span></div>"
    st.markdown(pistas_html, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        guess = st.text_input("Tu predicción:", key="guess_input", placeholder="Escribe el país...")
    with col2:
        if st.button("Enviar", key="btn_send"):
            if guess:
                jugar_turno(guess)
            else:
                st.error("Escribe un nombre.")

    st.markdown("---")
    st.subheader("Historial:")
    for h in st.session_state.historial:
        st.write(h)
