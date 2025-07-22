
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Configuración de la página
st.set_page_config(page_title="Banco Tampico Madero - Evaluador de Riesgo", layout="centered")

# Encabezado institucional
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>🏛️ Banco Tampico Madero</h1>
<h3 style='text-align: center;'>Evaluador de Riesgo Crediticio</h3>
<hr>
""", unsafe_allow_html=True)

# Cargar modelo
@st.cache_resource
def cargar_modelo():
    df = pd.read_csv("clientes_ficticios_con_nombres.csv")
    le = LabelEncoder()
    df["clasificación_encoded"] = le.fit_transform(df["clasificación"])
    X = df.drop(columns=["cliente_id", "nombre", "clasificación", "clasificación_encoded"])
    y = df["clasificación_encoded"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, le

modelo, label_encoder = cargar_modelo()

# Formulario
with st.form("formulario_cliente"):
    nombre = st.text_input("👤 Nombre del cliente")
    edad = st.number_input("🎂 Edad", min_value=18, max_value=100, step=1)
    ingresos = st.number_input("💵 Ingresos mensuales (MXN)", min_value=0, step=100)
    deuda = st.number_input("💳 Deuda total (MXN)", min_value=0, step=100)
    dias_mora = st.number_input("📅 Días en mora", min_value=0, max_value=365, step=1)
    historial_moras = st.number_input("📈 Historial de moras anteriores", min_value=0, max_value=20, step=1)
    contactado = st.selectbox("📞 ¿Ha sido contactado?", ["Sí", "No"])
    zona = st.selectbox("🌐 Zona de riesgo", ["Baja", "Media", "Alta"])
    visitas = st.number_input("🏠 Visitas previas al domicilio", min_value=0, max_value=10, step=1)

    enviado = st.form_submit_button("📊 Evaluar riesgo")

if enviado:
    # Convertir datos
    datos = pd.DataFrame([{
        "edad": edad,
        "ingresos_mensuales": ingresos,
        "deuda_total": deuda,
        "dias_mora": dias_mora,
        "historial_moras": historial_moras,
        "contactado": 1 if contactado == "Sí" else 0,
        "zona_riesgo": {"Baja": 1, "Media": 2, "Alta": 3}[zona],
        "visitas_previas": visitas
    }])

    # Predicción
    pred = modelo.predict(datos)[0]
    clase = label_encoder.inverse_transform([pred])[0]

    # Resultado con estilo
    st.markdown(f"""<div style='border-radius: 10px; padding: 20px; background-color: #D5F5E3;'>
    <h4>🧾 Resultado para <b>{nombre or 'cliente'}</b>:</h4>
    <h2 style='color: #117864;'>Clasificación: {clase.upper()}</h2>
    </div>""", unsafe_allow_html=True)
