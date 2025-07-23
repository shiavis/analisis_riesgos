
import streamlit as st
import pandas as pd
import openai
import os

st.set_page_config(page_title="Informe de Cartera Vencida - Banco Tampico Madero", layout="wide")

st.markdown("## 🏛️ Banco Tampico Madero")
st.markdown("### 📊 Generador Inteligivo de Informes de Cartera Vencida")
st.markdown("---")

# Clave de API (poner como variable de entorno o manualmente para prueba)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...")

archivo = st.file_uploader("📂 Sube tu archivo Excel o CSV de cartera vencida", type=["csv", "xlsx"])

if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)

    if st.button("📈 Calcular indicadores"):
        try:
            total_clientes = len(df)
            vencidos = df[df["estado"] == "Vencido"]
            total_vencidos = len(vencidos)
            monto_total_en_riesgo = vencidos["monto_credito"].sum()
            mora_promedio = round(vencidos["dias_mora"].mean(), 2)
            mora_maxima = vencidos["dias_mora"].max()
            zona_mas_critica = vencidos["zona"].value_counts().idxmax()
            no_contactados = len(vencidos[vencidos["contactado"] == "No"])
            mayores_60 = len(vencidos[vencidos["dias_mora"] > 60])
            porcentaje_vencidos = round((total_vencidos / total_clientes) * 100, 2)
            producto_mas_vencido = vencidos["producto"].value_counts().idxmax()

            st.success("✅ Indicadores calculados con éxito:")

            st.markdown(f'''
- Total de clientes: **{total_clientes}**
- Clientes vencidos: **{total_vencidos}**
- % de vencidos: **{porcentaje_vencidos}%**
- Monto total en riesgo: **${monto_total_en_riesgo:,.2f}**
- Mora promedio: **{mora_promedio} días**
- Mora máxima: **{mora_maxima} días**
- Zona más crítica: **{zona_mas_critica}**
- Clientes no contactados: **{no_contactados}**
- Clientes con mora > 60 días: **{mayores_60}**
- Producto más riesgoso: **{producto_mas_vencido}**
''')

            if st.button("🧠 Generar informe con IA"):
                prompt = (
                    "Eres un analista de riesgos de Banco Tampico Madero. "
                    "Con base en los siguientes indicadores, redacta un informe ejecutivo en español formal de 2 a 3 párrafos "
                    "con lenguaje claro y profesional. Finaliza con 2 recomendaciones concretas.\n\n"
                    f"Indicadores:\n"
                    f"- Total de clientes: {total_clientes}\n"
                    f"- Clientes vencidos: {total_vencidos}\n"
                    f"- Porcentaje vencidos: {porcentaje_vencidos}%\n"
                    f"- Monto total en riesgo: {monto_total_en_riesgo}\n"
                    f"- Mora promedio: {mora_promedio} días\n"
                    f"- Mora máxima: {mora_maxima} días\n"
                    f"- Zona con más vencidos: {zona_mas_critica}\n"
                    f"- No contactados: {no_contactados}\n"
                    f"- Clientes con mora > 60 días: {mayores_60}\n"
                    f"- Producto más vencido: {producto_mas_vencido}\n"
                )

                respuesta = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un experto en riesgo bancario y redacción ejecutiva."},
                        {"role": "user", "content": prompt}
                    ]
                )

                st.markdown("---")
                st.subheader("📄 Informe ejecutivo generado:")
                st.markdown(respuesta.choices[0].message.content)

        except Exception as e:
            st.error(f"Ocurrió un error al procesar el archivo: {e}")
