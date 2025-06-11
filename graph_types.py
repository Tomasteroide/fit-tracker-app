import plotly.express as px
import pandas as pd

def graph_excercise(data, ejercicio_seleccionado,metrica):

    df_filtrado = data[data["Ejercicio"] == ejercicio_seleccionado]

    
    if df_filtrado.empty:
        return "No hay datos para este ejercicio."
    
    df_filtrado["Fecha"] = pd.to_datetime(df_filtrado["Fecha"])
    
    fig = px.line(
        df_filtrado,
        x="Fecha",
        y=metrica,
        color="Progresión",
        title=f"Progreso en {ejercicio_seleccionado}({metrica})",
        labels={"Fecha": "Fecha", metrica: metrica},
        markers=True
    )
    
    fig.update_layout(xaxis_title="Fecha", yaxis_title=metrica)
    
    return fig



