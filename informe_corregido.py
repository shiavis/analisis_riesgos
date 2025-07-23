
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
- Clientes no contactados: {no_contactados}
- Clientes con mora > 60 días: {mayores_60}
- Producto más riesgoso: {producto_mas_vencido}
"""

    with st.spinner("Generando informe..."):
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un experto en análisis financiero."},
                {"role": "user", "content": prompt}
            ]
        )
        informe = respuesta.choices[0].message.content
        st.success("Informe generado con éxito:")
        st.markdown(informe)
