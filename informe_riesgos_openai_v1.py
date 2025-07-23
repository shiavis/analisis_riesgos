
import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="Análisis de Riesgos", layout="wide")

st.title("📊 Análisis de Riesgos de Crédito - Banco Tampico Madero")

archivo = st.file_uploader("Sube el archivo Excel con los datos de clientes", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        total_clientes = df.shape[0]
        total_vencidos = df[df['estado'] == 'Vencido'].shape[0]
        porcentaje_vencidos = (total_vencidos / total_clientes) * 100
        monto_total_en_riesgo = df[df['estado'] == 'Vencido']['monto_credito'].sum()
        mora_promedio = df['dias_mora'].mean()
        mora_maxima = df['dias_mora'].max()
        zona_mas_critica = df[df['estado'] == 'Vencido']['zona'].value_counts().idxmax()
        no_contactados = df[df['contactado'] == 'No'].shape[0]
        mayores_60 = df[df['dias_mora'] > 60].shape[0]
        producto_mas_vencido = df[df['estado'] == 'Vencido']['producto'].value_counts().idxmax()

        st.subheader("✅ Indicadores")
        st.markdown(f"""
        - Total de clientes: **{total_clientes}**
        - Clientes vencidos: **{total_vencidos}**
        - % de vencidos: **{porcentaje_vencidos:.2f}%**
        - Monto total en riesgo: **${monto_total_en_riesgo:,.2f}**
        - Mora promedio: **{mora_promedio:.1f} días**
        - Mora máxima: **{mora_maxima} días**
        - Zona más crítica: **{zona_mas_critica}**
        - Clientes no contactados: **{no_contactados}**
        - Clientes con mora > 60 días: **{mayores_60}**
        - Producto más riesgoso: **{producto_mas_vencido}**
        """)

        if st.button("🤖 Generar informe con IA"):
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            prompt = f"""
Eres un analista de riesgos de Banco Tampico Madero.
Con base en los siguientes indicadores, redacta un informe ejecutivo en español formal de 2 a 3 párrafos con lenguaje claro y profesional. Finaliza con 2 recomendaciones concretas.

Indicadores:
- Total de clientes: {total_clientes}
- Clientes vencidos: {total_vencidos}
- Porcentaje vencidos: {porcentaje_vencidos:.2f}%
- Monto total en riesgo: ${monto_total_en_riesgo:,.2f}
- Mora promedio: {mora_promedio:.1f} días
- Mora máxima: {mora_maxima} días
- Zona con más vencidos: {zona_mas_critica}
- No contactados: {no_contactados}
- Mora > 60 días: {mayores_60}
- Producto más riesgoso: {producto_mas_vencido}
"""

            respuesta = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            informe = respuesta.choices[0].message.content
            st.subheader("📝 Informe generado")
            st.write(informe)

    except Exception as e:
        st.error(f"Error al calcular los indicadores: {e}")
