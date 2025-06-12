import streamlit as st
import pandas as pd
from datetime import date
from functions.gsheet_utils import get_worksheet, leer_datos, guardar_datos
import plotly.express as px
from functions.graph_types import graph_excercise
from functions.editor import editar_ultimo_registro

st.set_page_config(page_title="Tracker Calistenia", layout="centered")
st.title("📊 Tracker de Progreso")

# Entradas
st.subheader("🔐 Registra entrenamiento")

fecha = st.date_input("Fecha", value=date.today())
ejercicio = st.selectbox("Ejercicio", ["Front Lever", "Planche", "Sentadilla", "Peso Muerto", "Peso corporal"])
progresion = st.selectbox("Progresión", ["Tuck", "Straddle", "Full", "Advanced", "Half Full","Sin progesión (peso libre)"])
peso = st.number_input("Peso (kg)", min_value=0, value=0, step=1)
reps_tiempo = st.text_input("Reps (Número) o Tiempo (s) (ej: Si son 10 repeticiones, escribe '10'. Si es un tiempo, escribe '30' para 30 segundos.)")
rir = st.number_input("RIR (Reps en reserva)", min_value=0, value=0, step=1)
estado_animico = st.selectbox("Estado anímico", ["Excelente", "Bueno", "Regular", "Malo", "Muy malo"])
comentario = st.text_area("Comentario opcional")

# Guardar
if st.button("Guardar sesión"):
    nueva_fila = pd.DataFrame([[fecha, ejercicio, progresion, peso,reps_tiempo, rir, estado_animico, comentario]],
                              columns=["Fecha", "Ejercicio", "Progresión", "Peso","Reps o Tiempo", "RIR", "Estado anímico","Comentario"])
    try:
        sheet = get_worksheet()
        data = leer_datos(sheet)
        data = pd.concat([data, nueva_fila], ignore_index=True)
    except:
        data = nueva_fila
        sheet = get_worksheet()
    guardar_datos(sheet, data)
    st.success("✅ Sesión guardada correctamente.")
    

# Historial
st.subheader("📖 Historial de entrenamientos")
try:
    sheet = get_worksheet()
    data = leer_datos(sheet)
    st.dataframe(data.sort_values("Fecha", ascending=False))
except:
    st.write("Aún no has registrado entrenamientos.")

#### Botón para activar edición
if "mostrar_editor" not in st.session_state:
    st.session_state.mostrar_editor = False

if st.button("✏️ Editar entrenamientos recientes"):
    st.session_state.mostrar_editor = not st.session_state.mostrar_editor


if st.session_state.mostrar_editor:
    editar_ultimo_registro()
    
    
    
    
    
    
## Graficar progreso

# Estadísticas y gráficar
st.subheader("📈 Visualización de entrenamientos")

try:
    sheet = get_worksheet()
    data = leer_datos(sheet)

    if not data.empty:
        ejercicio_seleccionado = st.selectbox(
            "Selecciona un ejercicio para graficar:",
            sorted(data["Ejercicio"].unique())
        )
        
        metrica = st.selectbox("Selecciona la métrica a graficar:", ["Peso", "Reps o Tiempo"])

        fig = graph_excercise(data, ejercicio_seleccionado, metrica)
        if isinstance(fig, str):
            st.write(fig)
        else:
            st.plotly_chart(fig) 
    else:
        st.write("No hay datos suficientes para graficar.")
except:
    st.write("Error al cargar los datos para la visualización.")
