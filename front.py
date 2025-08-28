import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point, Polygon
from datetime import datetime
import numpy as np

st.title("Análisis de Datos GPS y Biométricos con Ruta")

# Cargar automáticamente el fichero
try:
    df = pd.read_csv("datos_2025-06-04.csv")
except FileNotFoundError:
    st.error("No se encuentra el archivo 'datos_2025-06-04.csv'. Asegúrate de que está en el mismo directorio que este script.")
    st.stop()

# Preprocesamiento
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["vaca_id"] = df["vaca_id"].astype(str)

vaca_id = st.selectbox("Selecciona una vaca (ID de la vaca)", sorted(df["vaca_id"].unique()))
vaca_df = df[df["vaca_id"] == vaca_id]

hora_inicio = st.slider("Selecciona hora de inicio", 0, 23, 6)
hora_fin = st.slider("Selecciona hora de fin", 0, 23, 8)

filtrado = vaca_df[
    (vaca_df["timestamp"].dt.hour >= hora_inicio) &
    (vaca_df["timestamp"].dt.hour <= hora_fin)
].sort_values("timestamp")

st.write(f"{len(filtrado)} registros encontrados.")

# Zona de referencia
zona = Polygon([(41.38, 2.17), (41.384, 2.17), (41.384, 2.181), (41.38, 2.181)])

def analizar(row):
    punto = Point(row["lat"], row["lon"])
    en_zona = zona.contains(punto)
    temp_estado = "normal" if 36.0 <= row["temperatura"] <= 37.5 else "anómala"
    if row["frecuencia"] < 60:
        estado = "relajado"
    elif row["frecuencia"] < 100:
        estado = "normal"
    else:
        estado = "excitado"
    return en_zona, temp_estado, estado

resultados = filtrado.apply(lambda row: analizar(row), axis=1)
filtrado[["in_zone", "estado_temp", "estado_ritmo"]] = pd.DataFrame(resultados.tolist(), index=filtrado.index)

st.dataframe(filtrado[["timestamp", "lat", "lon", "temperatura", "estado_temp", "frecuencia", "estado_ritmo", "in_zone"]])

# Crear mapa
if len(filtrado) == 0:
    st.warning("No hay datos en el rango de horas seleccionado.")
else:
    m = folium.Map(location=[filtrado["lat"].mean(), filtrado["lon"].mean()], zoom_start=16)

    # Añadir zona de referencia
    folium.Polygon(
        locations=[(41.382, 2.178), (41.384, 2.178), (41.384, 2.181), (41.382, 2.181)],
        color="blue", fill=True, fill_opacity=0.1, tooltip="Zona de Referencia"
    ).add_to(m)

    # Añadir puntos individuales
    for _, row in filtrado.iterrows():
        color = "green" if row["in_zone"] else "red"
        folium.CircleMarker(
            location=(row["lat"], row["lon"]),
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            popup=(f"Hora: {row['timestamp'].time()}<br>"
                   f"Temp: {row['temperatura']}°C ({row['estado_temp']})<br>"
                   f"Frecuencia: {row['frecuencia']} bpm ({row['estado_ritmo']})<br>"
                   f"{'En zona' if row['in_zone'] else 'Fuera de zona'}")
        ).add_to(m)

    # Dibujar línea de ruta
    puntos_ruta = list(zip(filtrado["lat"], filtrado["lon"]))
    folium.PolyLine(puntos_ruta, color="purple", weight=3, opacity=0.7, tooltip="Ruta").add_to(m)

    st_folium(m, width=800, height=500)