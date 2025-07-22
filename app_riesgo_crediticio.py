
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Clasificación de Riesgo Crediticio", layout="wide")
st.title("🔍 Clasificador de Riesgo Crediticio de Clientes")

# Cargar modelo entrenado directamente (entrenamiento embebido para demo)
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

# Subida del archivo
archivo = st.file_uploader("📁 Sube un archivo CSV con datos de clientes", type=["csv"])

if archivo is not None:
    df_nuevo = pd.read_csv(archivo)

    columnas_esperadas = ['edad', 'ingresos_mensuales', 'deuda_total', 'dias_mora',
                          'historial_moras', 'contactado', 'zona_riesgo', 'visitas_previas']

    if all(col in df_nuevo.columns for col in columnas_esperadas):
        st.success("Archivo válido. Procesando predicciones...")

        X_nuevo = df_nuevo[columnas_esperadas]
        predicciones = modelo.predict(X_nuevo)
        etiquetas = label_encoder.inverse_transform(predicciones)

        df_nuevo['clasificación_predicha'] = etiquetas

        st.dataframe(df_nuevo)

        csv = df_nuevo.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Descargar resultados", csv, "resultados_crediticios.csv", "text/csv")
    else:
        st.error(f"Las columnas del archivo deben ser: {', '.join(columnas_esperadas)}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")



