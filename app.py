
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="PowerTechs Motor", layout="wide")

st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: black;'>
        <h1 style='color: gold;'>PowerTechs Motor</h1>
        <h3 style='color: white;'>ING. RONNY CALVA</h3>
        <p style='color: white;'>Control de mantenimiento vehicular</p>
    </div>
""", unsafe_allow_html=True)

if "db" not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=[
        "Placa", "Marca", "Modelo", "Año", "Fecha", "Kilometraje",
        "Tipo", "Descripción", "Comentario", "Técnico"
    ])

# Nuevo registro
st.sidebar.header("Nuevo registro de mantenimiento")
placa = st.sidebar.text_input("Placa del vehículo")
marca = st.sidebar.text_input("Marca")
modelo = st.sidebar.text_input("Modelo")
anio = st.sidebar.text_input("Año")
fecha = st.sidebar.date_input("Fecha", datetime.today())
km = st.sidebar.number_input("Kilometraje", 0)
tipo = st.sidebar.selectbox("Tipo de servicio", ["Mantenimiento", "Reparación", "Cambio"])
detalle = st.sidebar.text_area("Descripción del servicio")
comentario = st.sidebar.text_area("Comentario adicional (opcional)")
tecnico = st.sidebar.text_input("Técnico responsable")

if st.sidebar.button("Guardar registro"):
    nuevo_registro = {
        "Placa": placa,
        "Marca": marca,
        "Modelo": modelo,
        "Año": anio,
        "Fecha": fecha.strftime("%Y-%m-%d"),
        "Kilometraje": km,
        "Tipo": tipo,
        "Descripción": detalle,
        "Comentario": comentario,
        "Técnico": tecnico
    }
    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([nuevo_registro])], ignore_index=True)
    st.success("¡Registro guardado exitosamente!")

# Mostrar y editar historial
st.header("Historial de mantenimiento")
placa_buscar = st.text_input("Buscar por placa")
df_filtered = st.session_state.db[st.session_state.db["Placa"].str.contains(placa_buscar, case=False)] if placa_buscar else st.session_state.db

for i, row in df_filtered.iterrows():
    with st.expander(f"🚗 {row['Placa']} - {row['Marca']} {row['Modelo']} {row['Año']}"):
        with st.form(f"edit_form_{i}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                new_placa = st.text_input("Placa", row['Placa'], key=f"placa_{i}")
                new_marca = st.text_input("Marca", row['Marca'], key=f"marca_{i}")
                new_modelo = st.text_input("Modelo", row['Modelo'], key=f"modelo_{i}")
                new_anio = st.text_input("Año", row['Año'], key=f"anio_{i}")
            with col2:
                new_fecha = st.date_input("Fecha", datetime.strptime(row['Fecha'], "%Y-%m-%d"), key=f"fecha_{i}")
                new_km = st.number_input("Kilometraje", value=int(row['Kilometraje']), key=f"km_{i}")
                new_tipo = st.selectbox("Tipo", ["Mantenimiento", "Reparación", "Cambio"], index=["Mantenimiento", "Reparación", "Cambio"].index(row['Tipo']), key=f"tipo_{i}")
            with col3:
                new_detalle = st.text_area("Descripción", row['Descripción'], key=f"detalle_{i}")
                new_comentario = st.text_area("Comentario", row['Comentario'], key=f"comentario_{i}")
                new_tecnico = st.text_input("Técnico", row['Técnico'], key=f"tecnico_{i}")

            submitted = st.form_submit_button("💾 Guardar cambios")
            if submitted:
                st.session_state.db.loc[i] = {
                    "Placa": new_placa,
                    "Marca": new_marca,
                    "Modelo": new_modelo,
                    "Año": new_anio,
                    "Fecha": new_fecha.strftime("%Y-%m-%d"),
                    "Kilometraje": new_km,
                    "Tipo": new_tipo,
                    "Descripción": new_detalle,
                    "Comentario": new_comentario,
                    "Técnico": new_tecnico
                }
                st.success("Registro actualizado correctamente.")
                st.experimental_rerun()

        if st.button("🗑️ Eliminar este registro", key=f"delete_{i}"):
            st.session_state.db.drop(index=i, inplace=True)
            st.session_state.db.reset_index(drop=True, inplace=True)
            st.success("Registro eliminado correctamente.")
            st.experimental_rerun()
