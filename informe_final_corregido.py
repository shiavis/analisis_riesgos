
import streamlit as st
import pandas as pd
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Usa tu clave real si estás local

st.set_page_config(page_title="Análisis de Riesgos", layout="wide")
st.title("📊 Análisis de Riesgos de Cartera")

archivo = st.file_uploader("Carga el archivo Excel con los datos", type=["xlsx"])

if archivo is not None:
    try:
        df = pd.read_excel(archivo)

        total_clientes = df.shape[0]
        total_vencidos = df[df['estado'] == 'Vencido'].shape[0]
        porcentaje_vencidos = round((total_vencidos / total_clientes) * 100, 1)
        monto_total_en_riesgo = df[df['estado'] == 'Vencido']['monto_credito'].sum()
        mora_promedio = round(df[df['estado'] == 'Vencido']['dias_mora'].mean(), 2)
        mora_maxima = df[df['estado'] == 'Vencido']['dias_mora'].max()
        zona_mas_critica = df[df['estado'] == 'Vencido']['zona'].mode()[0]
        no_contactados = df[(df['estado'] == 'Vencido') & (df['contactado'] == 'No')].shape[0]
        mayores_60 = df[(df['estado'] == 'Vencido') & (df['dias_mora'] > 60)].shape[0]
        producto_mas_vencido = df[df['estado'] == 'Vencido']['producto'].mode()[0]

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
            - Mora > 60 días: {mayores_60}
            - Producto más riesgoso: {producto_mas_vencido}
            """

            with st.spinner("Generando informe con IA..."):
                respuesta = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                texto = respuesta.choices[0].message.content
                st.subheader("📝 Informe generado:")
                st.write(texto)

    except Exception as e:
        st.error(f"Error al calcular los indicadores: {e}")
