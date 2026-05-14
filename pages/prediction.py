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

/* Encabezado principal con sombra y gradiente */
.stApp h1 {{
    color: #fff8f0;
    font-size: 4.5rem;
    font-weight: bold;
    padding: 1.2rem 2rem 1.2rem 2rem;
    border-radius: 1.5rem;
    margin-bottom: 2rem;
    text-shadow: 0 2px 8px rgba(255, 183, 94, 0.85);
    display: inline-block;
}}

/* Parrafos destacados */
.stApp p, .stApp .stMarkdown p {{
    color: #fff8f0;
    border-radius: 1rem;
    padding: 1rem 2rem;
    font-size: 1.5rem;
    font-weight: 500;
    margin: 2rem 0;
    text-shadow: 0 2px 8px rgba(255, 183, 94, 0.85);
    text-align: center;
    justify-content: center;
}}

/* Tarjetas y contenedores */
.stApp .stDataFrame, .stApp .stTable, .stApp .stAlert, .stApp .stMarkdown, .stApp .stButton, .stApp .stNumberInput, .stApp .stSelectbox {{
    background: #3d2c1ecc !important;
    border-radius: 1.2rem !important;
    box-shadow: 0 2px 16px 0 rgba(255, 183, 94, 0.10);
    color: #fff8f0 !important;
    text-align: center;
    justify-content: center;
}}

/* Botones modernos */
.stApp button, .stApp .stButton>button{{
    background: linear-gradient(90deg, #FF8C69 0%, #ffecd0 100%) !important;
    border: none !important; 
    border-radius: 1.2rem !important;
    font-weight: bold !important;
    font-size: 1.2rem !important;
    box-shadow: 0 4px 10px 0 #fff8f0CC;
    transition: background 0.3s, color 0.3s;
    text-align: center;
}}
.stApp button:hover, .stApp .stButton>button:hover {{
    background: linear-gradient(90deg, #ffecd0 0%, #FF8C69 100%) !important;
    color: #a65c00 !important;
}}

/* Inputs y selectores */
.stApp input, .stApp select, .stApp textarea {{
    color: rgba(255, 248, 240) !important;
    font-size: 1.1rem !important;
}}

/* Sidebar translúcido */
[data-testid="stSidebar"] {{
    background: rgba(100, 100, 100, 0.7) !important;
    border-radius: 1.5rem 0 0 1.5rem;
    box-shadow: 2px 0 16px 0 rgba(255, 183, 94, 0.10);
}}

/* Scrollbar personalizado */
::-webkit-scrollbar {{
    width: 10px;
    background: #ffecd0;
}}
::-webkit-scrollbar-thumb {{
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

# Selector de país
pais = st.selectbox("🌍 Filtrar por país:", paises)


# Selector de año para predecir todos los meses
from datetime import datetime
import matplotlib.pyplot as plt

# Definir rango de años posibles (1950 a 2050 por ejemplo)
year = st.number_input("Año de predicción:", min_value=2013, max_value=2050, value=2026, step=1)

# Botón para ejecutar la predicción anual
if st.button("Predecir año completo"):
    try:
        # Cargar el modelo correspondiente al país seleccionado
        import joblib
        import numpy as np
        import os
        import pandas as pd

        # Normalizar nombre del país para el archivo
        safe_name = pais.replace(" ", "_").replace("/", "_")
        modelo_path = os.path.join("models", "modelos_hibridos_v2", f"{safe_name}.joblib")

        if not os.path.exists(modelo_path):
            st.error(f"No existe modelo para {pais}")
        else:
            artifact = joblib.load(modelo_path)
            reg = artifact['reg']
            model_arima = artifact['model_arima']
            n_train = artifact['n_train']
            # Predecir los 12 meses del año seleccionado
            # El último dato histórico es dic 2012 (n_train meses desde 1950-01)
            # Queremos predecir desde enero hasta diciembre del año seleccionado
            start_month = (year - 1950) * 12
            months = list(range(1, 13))
            # Generar fechas futuras
            future_dates = pd.date_range(start=pd.Timestamp(f"{year}-01-01"), periods=12, freq='MS')
            t_future = np.arange(start_month, start_month + 12)
            months_future = future_dates.month
            # Matriz de diseño para la parte determinista
            X_future = np.column_stack([
                t_future,
                *[(months_future == m).astype(int) for m in range(1, 12)]
            ])
            pred_det = reg.predict(X_future)
            # Componente ARIMA
            n_periods = (year - 2012) * 12
            if n_periods <= 0:
                st.warning("El año debe ser posterior a 2012 (fin de datos históricos)")
            pred_arima_full, ci_arima_full = model_arima.predict(n_periods=n_periods + 12, return_conf_int=True)
            # Solo nos interesan los últimos 12 meses (del año seleccionado)
            pred_arima = pred_arima_full[-12:]
            ci_lo = ci_arima_full[-12:, 0]
            ci_hi = ci_arima_full[-12:, 1]
            # Predicción final y bandas
            pred_final = pred_det + pred_arima
            conf_lower_final = pred_det + ci_lo
            conf_upper_final = pred_det + ci_hi

            # Crear gráfico
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(months, pred_final, label='Predicción', color='royalblue', marker='o')
            ax.fill_between(months, conf_lower_final, conf_upper_final, color='skyblue', alpha=0.3, label='Intervalo 95%')
            ax.set_xticks(months)
            ax.set_xticklabels([datetime(2000, m, 1).strftime('%b') for m in months])
            ax.set_xlabel('Mes')
            ax.set_ylabel('Temperatura Media (°C)')
            ax.set_title(f'Predicción mensual para {pais} en {year}')
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

            # Mostrar tabla resumen
            st.dataframe({
                'Mes': [datetime(2000, m, 1).strftime('%B') for m in months],
                'Predicción (°C)': np.round(pred_final, 2),
                'Confianza Inferior (°C)': np.round(conf_lower_final, 2),
                'Confianza Superior (°C)': np.round(conf_upper_final, 2)
            })
            st.caption("La predicción y el intervalo de confianza se basan en el modelo híbrido entrenado hasta 2012.")
    except Exception as e:
        st.error(f"Error en la predicción: {e}")


# Mensaje informativo si se selecciona país
if pais != "Todos":
    st.success(f"Mostrando datos para: {pais}")
else:
    st.info("Mostrando datos globales")