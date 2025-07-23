import streamlit as st
import pandas as pd
import openai
import os

st.set_page_config(page_title="Análisis de Cartera Vencida", page_icon="📊", layout="centered")

st.title("📊 Análisis de Riesgos - Cartera Vencida")

uploaded_file = st.file_uploader("Carga el archivo Excel con la cartera:", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if st.button("🧮 Calcular indicadores"):
        try:
            total_clientes = df.shape[0]
            total_vencidos = df[df['estado'].str.strip() == 'Vencido'].shape[0]
            porcentaje_vencidos = (total_vencidos / total_clientes) * 100

            monto_total_en_riesgo = df[df['estado'].str.strip() == 'Vencido']['pnto_credi'].sum()
            mora_promedio = df[df['estado'].str.strip() == 'Vencido']['dias_mora'].mean()
            mora_maxima = df[df['estado'].str.strip() == 'Vencido']['dias_mora'].max()

            zona_mas_critica = df[df['estado'].str.strip() == 'Vencido']['zona'].mode()[0]
            no_contactados = df[df['contactado'].str.strip() == 'No'].shape[0]
            mayores_60 = df[df['dias_mora'] > 60].shape[0]
            producto_mas_vencido = df[df['estado'].str.strip() == 'Vencido']['producto'].mode()[0]

            st.success("✅ Indicadores calculados con éxito:")
            st.markdown(f"""
- Total de clientes: **{total_clientes}**  
- Clientes vencidos: **{total_vencidos}**  
- % de vencidos: **{porcentaje_vencidos:.1f}%**  
- Monto total en riesgo: **${monto_total_en_riesgo:,.2f}**  
- Mora promedio: **{mora_promedio:.2f} días**  
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
- Porcentaje vencidos: {porcentaje_vencidos:.1f}%
- Monto total en riesgo: ${monto_total_en_riesgo:,.2f}
- Mora promedio: {mora_promedio:.2f} días
- Mora máxima: {mora_maxima} días
- Zona con más vencidos: {zona_mas_critica}
- Clientes no contactados: {no_contactados}
- Mora mayor a 60 días: {mayores_60}
- Producto más riesgoso: {producto_mas_vencido}
"""

                openai.api_key = os.getenv("OPENAI_API_KEY")
                respuesta = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                st.subheader("📝 Informe generado:")
                st.write(respuesta["choices"][0]["message"]["content"])

        except Exception as e:
            st.error(f"Error al calcular los indicadores: {str(e)}")