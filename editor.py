import streamlit as st
import pandas as pd
from gsheet_utils import get_worksheet, leer_datos, guardar_datos

def editar_ultimo_registro():
    sheet = get_worksheet()
    data = leer_datos(sheet)

    if data.empty:
        st.info("Aún no hay entrenamientos para editar.")
        return

    data_filtrada = data.copy()
    data_filtrada["Fecha"] = pd.to_datetime(data["Fecha"])
    ultimos = data_filtrada.sort_values("Fecha", ascending=False)

    st.write("Últimos registros del ejercicio seleccionado:")
    st.dataframe(ultimos)
    
    opciones_prog = ["Tuck", "Straddle", "Full", "Advanced", "Half Full", "Sin progesión (peso libre)"]
    opciones_ejercicio = ["Front Lever", "Planche", "Sentadilla", "Peso Muerto", "Peso corporal"]

    if not ultimos.empty:
        idx = st.number_input("Selecciona el número de fila a editar (según índice de tabla)", 
                              min_value=ultimos.index.min(), 
                              max_value=ultimos.index.max(), 
                              step=1)

        row = data.loc[idx]

        valor_prog = row["Progresión"]
        index_prog = opciones_prog.index(valor_prog) if valor_prog in opciones_prog else 0
        nueva_progresion = st.selectbox(
            "Progresión",
            opciones_prog,
            index=index_prog,
            key=f"progresion_edit_{idx}"
        )

        valor_ejercicio = row["Ejercicio"]
        index_ejercicio = opciones_ejercicio.index(valor_ejercicio) if valor_ejercicio in opciones_ejercicio else 0
        nuevo_ejercicio = st.selectbox(
            "Ejercicio",
            opciones_ejercicio,
            index=index_ejercicio,
            key=f"ejercicio_{idx}"
        )
        
        nueva_fecha = st.date_input("Fecha", value=pd.to_datetime(row["Fecha"]), key=f"fecha_edit_{idx}")

        peso_valor = 0 if pd.isna(row["Peso"]) else int(row["Peso"])
        nuevo_peso = st.number_input("Peso", min_value=0, value=peso_valor, key=f"peso_{idx}")
        nuevas_reps = st.text_input("Reps o Tiempo", value=str(row["Reps o Tiempo"]))
        nuevo_rir = st.slider("RIR", 0, 4, value=int(row["RIR"]))
        nuevo_estado = st.selectbox("Estado anímico", ["Excelente", "Bueno", "Regular", "Malo", "Muy malo"], index=["Excelente", "Bueno", "Regular", "Malo", "Muy malo"].index(row["Estado anímico"]),key=f"estado_{idx}")
        nuevo_comentario = st.text_area("Comentario", value=row["Comentario"])
        

        if st.button("Guardar cambios"):
            data.at[idx, "Fecha"] = nueva_fecha
            data.at[idx, "Ejercicio"] = nuevo_ejercicio
            data.at[idx, "Progresión"] = nueva_progresion
            data.at[idx, "Peso"] = nuevo_peso
            data.at[idx, "Reps o Tiempo"] = nuevas_reps
            data.at[idx, "RIR"] = nuevo_rir
            data.at[idx, "Estado anímico"] = nuevo_estado
            data.at[idx, "Comentario"] = nuevo_comentario

            guardar_datos(sheet, data)
            st.success("✅ Registro actualizado correctamente.")
            st.session_state.mostrar_editor = False
            st.rerun()
        if st.button("Eliminar registro 🗑️"):
            confirmar = st.checkbox("¿Estás seguro de que quieres eliminar este registro?", key=f"confirmar_{idx}")
        
            if confirmar:
                data = data.drop(index=idx).reset_index(drop=True)
                guardar_datos(sheet, data)
                st.success("🗑️ Registro eliminado correctamente.")
                st.session_state.mostrar_editor = False
                st.rerun()

