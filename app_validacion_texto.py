import pandas as pd
import streamlit as st
from datetime import date
from PIL import Image
import os

st.set_page_config(page_title="Club Park - Reporte Operativo", page_icon="🚗", layout="wide")

# Cabecera institucional con el Logotipo integrado
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    # Carga automática del logotipo local si se encuentra en la misma carpeta
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
        recibe = st.text_input("👤 Quien Recibe Reporte (Nombre)*", placeholder="Ej. Jesús")

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
        # Validación estricta obligatoria
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
        st.rerun()
        
