import streamlit as st
from operation_validator import extract_text_data, validate_operations

st.title("Validador automático de operaciones")
st.caption("Solo lectura de texto OCR; no se hacen inferencias visuales.")

texto = st.text_area("Texto OCR del reporte", height=350)
if st.button("Validar operación"):
    if not texto.strip():
        st.warning("Ingresa el texto OCR.")
    else:
        r = validate_operations(extract_text_data(texto))
        if r["estado"] == "VALIDO":
            st.success("✅ OPERACIÓN VÁLIDA")
        elif r["estado"] == "INVALIDO":
            st.error("❌ OPERACIÓN INVÁLIDA")
        else:
            st.warning("🟡 VALIDACIÓN PENDIENTE")
        st.json(r)
