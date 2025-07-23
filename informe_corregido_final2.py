
import streamlit as st
import pandas as pd
from io import BytesIO
from openai import OpenAI

st.title("📊 Análisis de Cartera Vencida - Banco Tampico Madero")

uploaded_file = st.file_uploader("Sube el archivo Excel de cartera vencida", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()  # Eliminar espacios en los nombres de columnas

    if st.button("📉 Calcular indicadores"):
        total_clientes = df.shape[0]
        total_vencidos = df[df['Estatus'] == 'Vencido'].shape[0]
        porcentaje_vencidos = round((total_vencidos / total_clientes) * 100, 1)
        monto_total_en_riesgo = df[df['Estatus'] == 'Vencido']['Monto'].sum()
        mora_promedio = round(df[df['Estatus'] == 'Vencido']['Mora (días)'].mean(), 2)
        mora_maxima = int(df[df['Estatus'] == 'Vencido']['Mora (días)'].max())
        zona_mas_critica = df[df['Estatus'] == 'Vencido']['Zona'].value_counts().idxmax()
        no_contactados = df[df['Contacto'] == 'No'].shape[0]
        mayores_60 = df[df['Mora (días)'] > 60].shape[0]
        producto_mas_vencido = df[df['Estatus'] == 'Vencido']['Producto'].value_counts().idxmax()

        st.success("✅ Indicadores calculados con éxito:")
        st.markdown(f"""
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
        """)

        if st.button("🧠 Generar informe con IA"):
            prompt = f"""
Eres un analista de riesgos de Banco Tampico Madero.
Con base en los siguientes indicadores, redacta un informe ejecutivo en español formal de 2 a 3 párrafos 
con lenguaje claro y profesional. Finaliza con 2 recomendaciones concretas.

Indicadores:
- Total de clientes: {total_clientes}
- Clientes vencidos: {total_vencidos}
- Porcentaje vencidos: {porcentaje_vencidos}%
- Monto total en riesgo: ${monto_total_en_riesgo:,.2f}
- Mora promedio: {mora_promedio} días
- Mora máxima: {mora_maxima} días
- Zona con más vencidos: {zona_mas_critica}
- No contactados: {no_contactados}
- Clientes con mora > 60 días: {mayores_60}
- Producto más riesgoso: {producto_mas_vencido}
"""

            import openai
            import os
            openai.api_key = os.getenv("OPENAI_API_KEY")
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            st.subheader("📄 Informe generado:")
            st.write(response.choices[0].message.content)
