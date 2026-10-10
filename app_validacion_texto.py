import pandas as pd
import streamlit as st
from datetime import date
from PIL import Image

st.set_page_config(page_title="Club Park - Reporte Operativo", page_icon="🚗", layout="centered")

st.title("🚗 Club Park Valet y Estacionamientos")
st.subheader("Control Operativo y Registro Semanal con Fotografía")

# Inicializar almacenamiento en la sesión de Streamlit
if "registros" not in st.session_state:
    st.session_state.registros = []

with st.form("form_reporte"):
    st.markdown("### 1. Evidencia Fotográfica del Reporte")
    foto_reporte = st.file_uploader("Tomar o subir foto de la hoja de reporte", type=["jpg", "jpeg", "png"])
    
    if foto_reporte is not None:
        # Mostrar vista previa de la foto en la aplicación
        imagen = Image.open(foto_reporte)
        st.image(imagen, caption="Vista previa del reporte físico", use_container_width=True)

    st.markdown("---")
    st.markdown("### 2. Captura y Verificación de Datos")
    
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha del Reporte", value=date.today())
        unidad = st.text_input("Unidad / Sucursal", placeholder="Ej. Sushiitto")
        costo_boleto = st.number_input("Costo del Boleto ($)", value=40, step=1)
        sueldo_operador = st.number_input("Sueldo del Operador ($)", value=280, step=10)
        
    with col2:
        folio_inicial = st.number_input("Folio Inicial", value=0, step=1)
        folio_final = st.number_input("Folio Final", value=0, step=1)
        cancelados = st.number_input("Boletos Cancelados", value=0, step=1)
        perdidos = st.number_input("Boletos Pérdidos", value=0, step=1)

    # Cálculos automáticos en tiempo real dentro del formulario
    total_boletos = (folio_final - folio_inicial + 1) if folio_final >= folio_inicial else 0
    pagados = max(0, total_boletos - cancelados - perdidos)
    ingreso_bruto = pagados * costo_boleto
    ingreso_neto = ingreso_bruto - sueldo_operador

    st.markdown("---")
    st.markdown("### 3. Resumen Calculado Automáticamente")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Total Boletos", total_boletos)
    r2.metric("Pagados", pagados)
    r3.metric("Ingreso Bruto", f"${ingreso_bruto}")
    r4.metric("Ingreso Neto", f"${ingreso_neto}", delta=f"${ingreso_neto}")

    submitted = st.form_submit_button("💾 Guardar Registro en el Consolidado")
    
    if submitted:
        if not unidad.strip():
            st.warning("Por favor, ingresa el nombre de la unidad o sucursal.")
        else:
            nuevo_registro = {
                "Fecha": str(fecha),
                "Unidad": unidad,
                "Costo Boleto": costo_boleto,
                "Folio Inicial": folio_inicial,
                "Folio Final": folio_final,
                "Total Boletos": total_boletos,
                "Boletos Pagados": pagados,
                "Cancelados": cancelados,
                "Pérdidos": perdidos,
                "Sueldo Operador": sueldo_operador,
                "Ingreso Bruto": ingreso_bruto,
                "Ingreso Neto": ingreso_neto,
                "Tiene Foto": "Sí" if foto_reporte else "No"
            }
            st.session_state.registros.append(nuevo_registro)
            st.success(f"¡Reporte de la unidad '{unidad}' guardado correctamente con su evidencia!")

# Sección de visualización y exportación del consolidado semanal
if st.session_state.registros:
    st.markdown("---")
    st.markdown("### 📊 Consolidado Semanal Acumulado")
    df_registros = pd.DataFrame(st.session_state.registros)
    st.dataframe(df_registros, use_container_width=True)

    # Botón para descargar en CSV (compatible con Excel)
    csv_data = df_registros.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte Semanal en CSV (Excel)",
        data=csv_data,
        file_name="Reporte_Semanal_ClubPark.csv",
        mime="text/csv",
    )
    
    if st.button("🗑️ Limpiar Todos los Registros"):
        st.session_state.registros = []
        st.rerun()
        
