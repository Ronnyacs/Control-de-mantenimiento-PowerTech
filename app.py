
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="PowerTechs Motor", layout="wide")

# Título y encabezado
st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: black;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Logo.svg/512px-Logo.svg.png' width='100'>
        <h1 style='color: gold;'>PowerTechs Motor</h1>
        <h3 style='color: white;'>ING. RONNY CALVA</h3>
        <p style='color: white;'>Control de mantenimiento vehicular</p>
    </div>
""", unsafe_allow_html=True)

# Simulación de base de datos en memoria
if "db" not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Placa", "Fecha", "Kilometraje", "Tipo", "Descripción", "Técnico"])

st.sidebar.header("Nuevo registro de mantenimiento")
placa = st.sidebar.text_input("Placa del vehículo")
fecha = st.sidebar.date_input("Fecha", datetime.today())
km = st.sidebar.number_input("Kilometraje", 0)
tipo = st.sidebar.selectbox("Tipo de servicio", ["Mantenimiento", "Reparación", "Cambio"])
detalle = st.sidebar.text_area("Descripción del servicio")
tecnico = st.sidebar.text_input("Técnico responsable")
foto = st.sidebar.file_uploader("Foto adjunta (opcional)", type=["jpg", "png", "jpeg"])

if st.sidebar.button("Guardar registro"):
    nuevo_registro = {
        "Placa": placa,
        "Fecha": fecha.strftime("%Y-%m-%d"),
        "Kilometraje": km,
        "Tipo": tipo,
        "Descripción": detalle,
        "Técnico": tecnico
    }
    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([nuevo_registro])], ignore_index=True)
    st.success("¡Registro guardado exitosamente!")

st.header("Historial de mantenimiento")
placa_buscar = st.text_input("Buscar por placa")
if placa_buscar:
    resultado = st.session_state.db[st.session_state.db["Placa"].str.contains(placa_buscar, case=False)]
    st.dataframe(resultado)
else:
    st.dataframe(st.session_state.db)
