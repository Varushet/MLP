import streamlit as st
import pandas as pd
import streamlit as st
import base64
import os
import joblib

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

/* Encabezado principal con sombra y gradiente */
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

/* Parrafos destacados */
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

/* Tarjetas y contenedores */
.stApp .stDataFrame, .stApp .stTable, .stApp .stAlert, .stApp .stMarkdown, .stApp .stButton, .stApp .stNumberInput, .stApp .stSelectbox {{
    background: #102A43CC !important; 
    border-radius: 1.2rem !important;
    box-shadow: 0 2px 16px 0 #C0C0C0CC;
    color: #fff8f0 !important;
    text-align: center;
    justify-content: center;
}}

/* Botones modernos */
.stApp button, .stApp .stButton>button{{
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

/* Inputs y selectores */
.stApp input, .stApp select, .stApp textarea {{
    color: rgba(255, 248, 240) !important;
    font-size: 1.1rem !important;
}}

/* Sidebar translúcido */
[data-testid="stSidebar"] {{
    color: rgba(0, 0, 0) !important;
    background: rgba(208, 208, 208, 0.3) !important;
    border-radius: 1.5rem 0 0 1.5rem;
    box-shadow: 2px 0 16px 0 rgba(255, 183, 94, 0.10);
}}

/* Scrollbar personalizado */
::-webkit-scrollbar {{
    color: rgba(0, 0, 0) !important;
    width: 10px;
    background: #ffecd0;
}}
::-webkit-scrollbar-thumb {{
    color: rgba(0, 0, 0) !important;
    background: #ffb75e;
    border-radius: 8px;
}}

/* Mejorar contraste de widgets */
.stApp .stNumberInput input, .stApp .stSelectbox div {{
    color: rgba(255, 234, 208) !important;
}}

/* Ajuste de tabla resumen */
.stApp .stDataFrame th, .stApp .stDataFrame td {{
    background: rgba(255,255,255,0.85) !important;
    color: #3d2c1e !important;
}}

/* Mensajes de éxito y advertencia */
.stApp .stAlert[data-baseweb="notification"] {{
    background: linear-gradient(90deg, #ffecd0 0%, #ffb75e 100%) !important;
    color: #3d2c1e !important;
    border-radius: 1.2rem !important;
    box-shadow: 0 2px 8px 0 rgba(255, 183, 94, 0.10);
}}
</style>

<h1>A meteorology based game</h1>

<p>Match an AI to guess a country in the entire world based only on geographic and climatologic data.</p>

""", unsafe_allow_html=True)


# --- 1. CARGA DE RECURSOS REALES (usando modelo FinalLvL.pkl y dataset real) ---

@st.cache_resource
def cargar_recursos_juego():
    # Cargar dataset real (ajusta el path y columnas según tu dataset)
    df = pd.read_csv('data/climaDS.csv.gz')
    # Asegúrate de que las columnas estén en el orden correcto y con los nombres correctos
    # Ejemplo de columnas: ['Pais', 'Precipitacion', 'Temp_Media', 'Humedad', 'Horas_Sol', 'Altitud_Media', 'Latitude']
    # Si tu dataset tiene otros nombres, ajústalos aquí
    # Cargar modelo entrenado
    modelo = joblib.load('models/final_boss.pkl')
    # Crear label encoder para los países

    col_id = 'country_id'
    col_name = 'country'
    
    # Verificación básica por si acaso
    if col_id not in df.columns or col_name not in df.columns:
        st.error(f"Columnas no encontradas. Revisa que '{col_id}' y '{col_name}' existan en el CSV.")
        st.stop()

    # Definir el orden de las pistas (de menos a más informativas)
    all_features_model = ['precip_mm', 'cloud', 'latitude', 'wind_kph', 'humidity', 'Air_poll', 'sun_h', 'longitude'] 

    features_names = [
        ['precip_mm', 'cloud'],
        ['precip_mm', 'cloud', 'wind_kph'],
        ['precip_mm', 'cloud', 'wind_kph', 'humidity', 'Air_poll'],
        ['precip_mm', 'cloud', 'wind_kph', 'humidity', 'Air_poll', 'sun_h'],
        ['precip_mm', 'cloud', 'wind_kph', 'humidity', 'Air_poll', 'sun_h', 'longitude'],
        ['precip_mm', 'cloud', 'wind_kph', 'humidity', 'Air_poll', 'sun_h', 'longitude', 'latitude']
    ]
    return df, modelo, col_id, col_name, features_names, all_features_model


# Cargamos los recursos
df_juego, modelo_ia, col_id, col_name, lista_features, all_features_model = cargar_recursos_juego()

# Calcular medias de las features para rellenar valores no revelados
medias_features = df_juego[all_features_model].mean()

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


# Cambia la lógica: el juego solo termina si el jugador acierta o se acaban los intentos

# Ahora la IA usa el modelo real y se le van revelando más variables en cada turno
def jugar_turno(guess_jugador):
    if not st.session_state.juego_activo:
        return

    intentos_actuales = st.session_state.intentos
    # Obtener datos del país secreto seleccionado
    pais_secreto = st.session_state.pais_secreto_obj
    pais_real_nombre = pais_secreto[col_name]
    pais_real_id = pais_secreto[col_id]  # Usamos el ID directo del DF

    # 1. Evaluar Jugador
    if guess_jugador.strip().lower() == pais_real_nombre.lower():
        st.session_state.historial.append(f"✅ ¡GANASTE! Adivinaste {pais_real_nombre} en el intento {intentos_actuales + 1}.")
        st.session_state.juego_activo = False
        st.rerun()
        return

    # 2. Evaluar Máquina (la IA puede acertar, pero el juego sigue hasta que el jugador acierte o se acaben los intentos)
    # Revelar más variables en cada turno, hasta un máximo de las disponibles
    max_pistas = min(intentos_actuales + 1, len(lista_features))
    features_visibles = lista_features[max_pistas - 1]
    

    # Preparar input para el modelo (asegurar que sea DataFrame o array 2D)
    input_completo = pd.DataFrame(columns=all_features_model)
    # Rellenar las visibles con los datos reales
    for feat in features_visibles:
        if feat in all_features_model:
            input_completo[feat] = [pais_secreto[feat]]
    # Rellenar las NO visibles con la media
    for feat in all_features_model:
        if feat not in features_visibles:
            input_completo[feat] = [medias_features[feat]]

    # Asegurar el orden exacto de columnas del entrenamiento
    datos_input = input_completo[all_features_model].values.reshape(1, -1)
    
      
    # Predicción
    prediccion_id = modelo_ia.predict(datos_input)[0]
    
    # Buscar el nombre del país predicho por la IA usando el ID predicho
    # Filtramos el DF original para encontrar qué país tiene ese country_id
    prediccion_match = df_juego[df_juego[col_id] == int(prediccion_id)]
    
    if not prediccion_match.empty:
        pais_predicho_maquina = prediccion_match.iloc[0][col_name]
    else:
        pais_predicho_maquina = "Desconocido (ID no encontrado)"

    msg_maquina = f"🤖 **Turno {intentos_actuales + 1}:** La máquina apuesta por {pais_predicho_maquina}."

    # Comparar IDs para ver si acertó
    if int(prediccion_id) == int(pais_real_id):
        st.session_state.historial.append(msg_maquina + " 🏆 ¡La máquina ha acertado!")
    else:
        st.session_state.historial.append(msg_maquina + " ❌ Falló.")


    # Lógica de fin de juego
    st.session_state.intentos += 1
    if st.session_state.intentos >= 5:
        st.session_state.historial.append(f"💀 Fin del juego. Era {pais_real_nombre}.")
        st.session_state.juego_activo = False
        # Guardar el país secreto en el estado para mostrarlo después
        st.session_state.pais_secreto_final = pais_real_nombre
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
        st.rerun()
    # Mostrar el país secreto al final si existe
    if 'pais_secreto_final' in st.session_state:
        st.success(f"El país secreto era: {st.session_state.pais_secreto_final}")
        # Eliminarlo para la siguiente partida
        del st.session_state.pais_secreto_final
else:
    # Estamos EN JUEGO
    # Mostrar cuántas variables se revelan en este turno
    max_pistas = min(st.session_state.intentos + 1, len(lista_features))
    num_vars = len(lista_features[max_pistas - 1])
    st.markdown(f"### Ronda {st.session_state.intentos + 1}/5")
    st.caption(f"La máquina usa **{num_vars} variable(s)** climática(s). Se revelan: {', '.join(lista_features[max_pistas - 1])}")

    # Mostrar todas las pistas reveladas hasta el turno actual
    pistas_actuales = lista_features[max_pistas - 1]
    for var in pistas_actuales:
        valor_pista = st.session_state.pais_secreto_obj[var]
        st.metric(label=f"Pista: {var}", value=valor_pista)

    # Input y Botón
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