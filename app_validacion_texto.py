import pandas as pd
import streamlit as st
from datetime import date
from PIL import Image
import os

st.set_page_config(page_title="Club Park - Reporte Operativo", page_icon="🚗", layout="wide")

# Cabecera institucional con el Logotipo integrado
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=220)
    else:
        st.info("💡 Coloca tu imagen como 'logo.png' en la misma carpeta para mostrarla aquí.")
        st.markdown("### **CP** - Club Park")

with col_titulo:
    st.title("CLUB PARK VALET Y ESTACIONAMIENTOS S.A. DE C.V.")
    st.subheader("Sistema de Control Operativo y Validación de Flujo por Unidad")

# Inicializar almacenamiento de registros en sesión
if "registros" not in st.session_state:
    st.session_state.registros = []

st.markdown("---")
st.markdown("### 📸 1. Evidencia Fotográfica del Reporte Físico")
foto_reporte = st.file_uploader("Tomar o subir foto de la hoja de reporte", type=["jpg", "jpeg", "png"], key="foto")

if foto_reporte is not None:
    imagen = Image.open(foto_reporte)
    st.image(imagen, caption="Vista previa de la hoja de reporte física", width=350)

st.markdown("---")
st.markdown("### 📝 2. Captura Obligatoria de Datos del Reporte")
st.warning("⚠️ Todos los campos son obligatorios. La aplicación no permitirá guardar el registro si falta información clave.")

with st.form("form_reporte_completo"):
    c1, c2, c3 = st.columns(3)
    
    with c1:
        fecha = st.date_input("📅 Fecha", value=date.today())
        sitio = st.text_input("🏢 Sitio / Unidad*", placeholder="Ej. Sushiitto")
        costo_boleto = st.number_input("💵 Costo del Boleto ($)", value=40, step=1)
        folio_inicial = st.number_input("🔢 Folio Inicial Utilizado", value=0, step=1)
        folio_final = st.number_input("🔢 Folio Final Utilizado", value=0, step=1)
        folio_sin_desprender = st.number_input("🔖 Folio inicio sin desprender del block", value=0, step=1)

    with c2:
        total_boletos = st.number_input("🎟️ Total de Boletos", value=0, step=1)
        boletos_pagados = st.number_input("✅ Boletos Pagados", value=0, step=1)
        boletos_cancelados = st.number_input("❌ Boletos Cancelados", value=0, step=1)
        boletos_perdidos = st.number_input("⚠️ Boletos Pérdidos", value=0, step=1)
        total_boletos_entregados = st.number_input("📦 Total de Boletos Entregados", value=0, step=1)
        gastos_operacion = st.number_input("🛠️ Gastos de Operación ($)", value=0.0, step=10.0)

    with c3:
        lider_sueldo = st.number_input("👔 Líder de Unidad - Sueldo ($)", value=0.0, step=10.0)
        operador1_sueldo = st.number_input("👷 Operador 1 - Sueldo ($)", value=280.0, step=10.0)
        operador2_sueldo = st.number_input("👷 Operador 2 - Sueldo ($)", value=0.0, step=10.0)
        gastos_especiales = st.number_input("📌 Gastos Especiales ($)", value=0.0, step=10.0)
        gastos_generales = st.number_input("📋 Gastos Generales ($)", value=0.0, step=10.0)
        
    st.markdown("---")
    c4, c5 = st.columns(2)
    with c4:
        elaboro = st.text_input("✍️ Elaboró Reporte (Nombre)*", placeholder="Ej. Gaby")
    with c5:
        recibe = st.text_input("👤 Quien Recibe Report
                               
