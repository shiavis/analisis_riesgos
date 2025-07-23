
import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="Banco Tampico Madero", page_icon="🏦")

st.title("🏦 Banco Tampico Madero - Análisis de Cartera Vencida")

uploaded_file = st.file_uploader("Sube el archivo Excel de cartera vencida", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if st.button("📊 Calcular indicadores"):
        total_clientes = len(df)
        total_vencidos = df[df['Estatus'] == 'Vencido'].shape[0]
        porcentaje_vencidos = (total_vencidos / total_clientes) * 100
        monto_total_en_riesgo = df[df['Estatus'] == 'Vencido']['Monto'].sum()
        mora_promedio = df[df['Estatus'] == 'Vencido']['Mora (días)'].mean()
        mora_maxima = df[df['Estatus'] == 'Vencido']['Mora (días)'].max()
        zona_mas_critica = df[df['Estatus'] == 'Vencido']['Zona'].value_counts().idxmax()
        no_contactados = df[df['Contacto'] == 'No'].shape[0]
        mayores_60 = df[(df['Estatus'] == 'Vencido') & (df['Mora (días)'] > 60)].shape[0]
        producto_mas_vencido = df[df['Estatus'] == 'Vencido']['Producto'].value_counts().idxmax()

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
- No contactados: {no_contactados}
- Mora > 60 días: {mayores_60}
- Producto más riesgoso: {producto_mas_vencido}
"""

            with st.spinner("Generando informe..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                st.subheader("📄 Informe generado:")
                st.write(response.choices[0].message.content)
