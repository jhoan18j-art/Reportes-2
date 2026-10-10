import pandas as pd
import streamlit as st
from datetime import date
from PIL import Image
import os
import google.generativeai as genai
import json

st.set_page_config(page_title="Club Park - Reporte Inteligente", page_icon="🚗", layout="wide")

# Configurar API Key de Gemini (puedes ingresarla en la barra lateral o configurarla en los secrets de Streamlit)
st.sidebar.title("⚙️ Configuración de IA")
gemini_api_key = st.sidebar.text_input("Ingresa tu API Key de Gemini (Gratis)", type="password")

if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# Cabecera institucional con el Logotipo integrado
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=200)
    else:
        st.markdown("### **CP** - Club Park")

with col_titulo:
    st.title("CLUB PARK VALET Y ESTACIONAMIENTOS S.A. DE C.V.")
    st.subheader("Control Operativo Inteligente con Extracción por Fotografía (IA)")

# Inicializar almacenamiento de registros en sesión y datos extraídos
if "registros" not in st.session_state:
    st.session_state.registros = []

if "datos_ia" not in st.session_state:
    st.session_state.datos_ia = {}

st.markdown("---")
st.markdown("### 📸 1. Tomar o Subir Foto del Reporte Físico")
foto_reporte = st.file_uploader("Sube la fotografía de la hoja de reporte de operación", type=["jpg", "jpeg", "png"], key="foto_ia")

if foto_reporte is not None:
    imagen = Image.open(foto_reporte)
    st.image(imagen, caption="Fotografía del reporte físico", width=350)
    
    if gemini_api_key:
        if st.button("🤖 Analizar Fotografía con Inteligencia Artificial"):
            with st.spinner("Leyendo la hoja de reporte y extrayendo datos con IA..."):
                try:
                    # Usar Gemini 1.5 Flash para extraer los datos de la imagen
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = """
                    Analiza esta imagen de una hoja de reporte de operación de valet parking de Club Park Valet y Estacionamientos.
                    Extrae la siguiente información en formato JSON exacto:
                    {
                        "sitio": "nombre de la unidad o establecimiento (ej. Sushiitto)",
                        "costo_boleto": numero (ej. 40),
                        "folio_inicial": numero,
                        "folio_final": numero,
                        "folio_sin_desprender": numero (si no aparece, pon 0),
                        "total_boletos": numero,
                        "boletos_pagados": numero,
                        "boletos_cancelados": numero,
                        "boletos_perdidos": numero,
                        "total_entregados": numero,
                        "gastos_operacion": numero (si no aparece, pon 0),
                        "lider_sueldo": numero (si no aparece, pon 0),
                        "operador1_sueldo": numero (ej. 280),
                        "operador2_sueldo": numero (si no aparece, pon 0),
                        "gastos_especiales": numero (si no aparece, pon 0),
                        "gastos_generales": numero (si no aparece, pon 0),
                        "elaboro": "nombre de quien elaboró el reporte",
                        "recibe": "nombre de quien recibe el reporte"
                    }
                    Devuelve ÚNICAMENTE el objeto JSON válido, sin texto adicional.
                    """
                    response = model.generate_content([imagen, prompt])
                    # Limpiar respuesta JSON
                    texto_json = response.text.replace("```json", "").replace("```", "").strip()
                    st.session_state.datos_ia = json.loads(texto_json)
                    st.success("¡Datos extraídos con éxito por la Inteligencia Artificial!")
                except Exception as e:
                    st.error(f"Error al procesar la imagen con IA: {e}")
    else:
        st.info("💡 Ingresa tu API Key gratuita de Gemini en la barra lateral izquierda para activar el llenado automático por fotografía.")

# Obtener valores predeterminados (de la IA si ya se procesó, o vacíos/ceros)
d = st.session_state.datos_ia

st.markdown("---")
st.markdown("### 📝 2. Verificación y Corrección de Datos")
st.warning("⚠️ Revisa que los campos extraídos por la IA sean correctos antes de guardar.")

with st.form("form_reporte_completo"):
    c1, c2, c3 = st.columns(3)
    
    with c1:
        fecha = st.date_input("📅 Fecha", value=date.today())
        sitio = st.text_input("🏢 Sitio / Unidad*", value=d.get("sitio", ""))
        costo_boleto = st.number_input("💵 Costo del Boleto ($)", value=float(d.get("costo_boleto", 40)), step=1.0)
        folio_inicial = st.number_input("🔢 Folio Inicial Utilizado", value=int(d.get("folio_inicial", 0)), step=1)
        folio_final = st.number_input("🔢 Folio Final Utilizado", value=int(d.get("folio_final", 0)), step=1)
        folio_sin_desprender = st.number_input("🔖 Folio inicio sin desprender del block", value=int(d.get("folio_sin_desprender", 0)), step=1)

    with c2:
        total_boletos = st.number_input("🎟️ Total de Boletos", value=int(d.get("total_boletos", 0)), step=1)
        boletos_pagados = st.number_input("✅ Boletos Pagados", value=int(d.get("boletos_pagados", 0)), step=1)
        boletos_cancelados = st.number_input("❌ Boletos Cancelados", value=int(d.get("boletos_cancelados", 0)), step=1)
        boletos_perdidos = st.number_input("⚠️ Boletos Pérdidos", value=int(d.get("boletos_perdidos", 0)), step=1)
        total_boletos_entregados = st.number_input("📦 Total de Boletos Entregados", value=int(d.get("total_entregados", 0)), step=1)
        gastos_operacion = st.number_input("🛠️ Gastos de Operación ($)", value=float(d.get("gastos_operacion", 0.0)), step=10.0)

    with c3:
        lider_sueldo = st.number_input("👔 Líder de Unidad - Sueldo ($)", value=float(d.get("lider_sueldo", 0.0)), step=10.0)
        operador1_sueldo = st.number_input("👷 Operador 1 - Sueldo ($)", value=float(d.get("operador1_sueldo", 280.0)), step=10.0)
        operador2_sueldo = st.number_input("👷 Operador 2 - Sueldo ($)", value=float(d.get("operador2_sueldo", 0.0)), step=10.0)
        gastos_especiales = st.number_input("📌 Gastos Especiales ($)", value=float(d.get("gastos_especiales", 0.0)), step=10.0)
        gastos_generales = st.number_input("📋 Gastos Generales ($)", value=float(d.get("gastos_generales", 0.0)), step=10.0)
        
    st.markdown("---")
    c4, c5 = st.columns(2)
    with c4:
        elaboro = st.text_input("✍️ Elaboró Reporte (Nombre)*", value=d.get("elaboro", ""))
    with c5:
        recibe = st.text_input("👤 Quien Recibe Reporte (Nombre)*", value=d.get("recibe", ""))

    # Cálculos automáticos y financieros
    total_sueldos_nominas = lider_sueldo + operador1_sueldo + operador2_sueldo
    total_gastos = gastos_operacion + gastos_especiales + gastos_generales + total_sueldos_nominas
    ingreso_bruto = boletos_pagados * costo_boleto
    ingreso_neto = ingreso_bruto - total_gastos
    cantidad_entregar = ingreso_neto

    st.markdown("### 📊 Resumen Financiero Calculado")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Gastos y Nóminas", f"${total_gastos:,.2f}")
    m2.metric("Ingreso Bruto", f"${ingreso_bruto:,.2f}")
    m3.metric("Ingreso Neto", f"${ingreso_neto:,.2f}", delta=f"${ingreso_neto:,.2f}")
    m4.metric("Cantidad a Entregar", f"${cantidad_entregar:,.2f}")

    submitted = st.form_submit_button("💾 Validar y Guardar Registro en el Consolidado Semanal")

    if submitted:
        if not sitio.strip() or not elaboro.strip() or not recibe.strip():
            st.error("❌ Error de validación: Los campos 'Sitio / Unidad', 'Elaboró Reporte' y 'Quien Recibe Reporte' son obligatorios.")
        elif foto_reporte is None:
            st.warning("⚠️ Advertencia: Es necesario adjuntar la fotografía de la hoja de reporte físico.")
        else:
            nuevo_registro = {
                "Fecha": str(fecha),
                "Sitio / Unidad": sitio,
                "Costo Boleto": costo_boleto,
                "Folio Inicial": folio_inicial,
                "Folio Final": folio_final,
                "Folio sin desprender": folio_sin_desprender,
                "Total Boletos": total_boletos,
                "Boletos Pagados": boletos_pagados,
                "Cancelados": boletos_cancelados,
                "Pérdidos": boletos_perdidos,
                "Total Entregados": total_boletos_entregados,
                "Gastos Operación": gastos_operacion,
                "Líder Sueldo": lider_sueldo,
                "Operador 1 Sueldo": operador1_sueldo,
                "Operador 2 Sueldo": operador2_sueldo,
                "Gastos Especiales": gastos_especiales,
                "Total Gastos y Nóminas": total_gastos,
                "Gastos Generales": gastos_generales,
                "Ingreso Bruto": ingreso_bruto,
                "Ingreso Neto": ingreso_neto,
                "Cantidad a Entregar": cantidad_entregar,
                "Elaboró": elaboro,
                "Recibe": recibe,
                "Evidencia Foto": "Sí"
            }
            st.session_state.registros.append(nuevo_registro)
            st.success(f"¡El reporte del sitio '{sitio}' ha sido validado y guardado exitosamente!")

# Sección de visualización y exportación consolidada
if st.session_state.registros:
    st.markdown("---")
    st.markdown("### 📈 Consolidado Semanal Acumulado")
    df_reportes = pd.DataFrame(st.session_state.registros)
    st.dataframe(df_reportes, use_container_width=True)

    csv_export = df_reportes.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte Semanal Completo en CSV (Excel)",
        data=csv_export,
        file_name="Consolidado_Semanal_ClubPark.csv",
        mime="text/csv",
    )

    if st.button("🗑️ Limpiar Todos los Registros"):
        st.session_state.registros = []
        st.session_state.datos_ia = {}
        st.rerun()
        
