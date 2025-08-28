import csv
import os
import time
from datetime import datetime, timedelta
import random

ARCHIVO = "datos_2025-06-04.csv"
NUM_VACAS = 10
INTERVALO_MINUTOS = 10
NUM_MUESTRAS = 60  # 10 hora de datos
FECHA_BASE = datetime(2025, 6, 3, 6, 0)

def generar_datos_csv(nombre_archivo):
    print("🛠️ Generando archivo de datos simulado...")
    with open(nombre_archivo, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["vaca_id", "timestamp", "lat", "lon", "temperatura", "frecuencia", "enviado"])

        for muestra in range(NUM_MUESTRAS):
            timestamp = FECHA_BASE + timedelta(minutes=muestra * INTERVALO_MINUTOS)
            for pid in range(1, NUM_VACAS + 1):
                vaca_id = f"{pid:03d}"
                lat = 41.8 + random.uniform(-0.05, 0.05)
                lon = 2.30 + random.uniform(-0.05, 0.05)
                temp = round(random.uniform(36.0, 38.0), 1)
                frecuencia = random.randint(60, 120)
                writer.writerow([vaca_id, timestamp.isoformat() + "Z", lat, lon, temp, frecuencia, 0])
    print(f"✅ Archivo generado: {nombre_archivo}")

def enviar_a_la_nube(dato):
    print(f"🌐 Enviando: {dato}")
    time.sleep(0.005)  # Simula retardo de red
    return True

def procesar_y_actualizar_archivo(nombre_archivo):
    with open(nombre_archivo, mode="r", newline="") as f:
        reader = csv.reader(f)
        filas = list(reader)

    encabezado = filas[0]
    datos = filas[1:]

    datos_actualizados = []
    for row in datos:
        if row[-1] == '0':
            if enviar_a_la_nube(row):
                row[-1] = '1'
        datos_actualizados.append(row)

    with open(nombre_archivo, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(encabezado)
        writer.writerows(datos_actualizados)

# --------------------
# MAIN
# --------------------
if not os.path.exists(ARCHIVO):
    generar_datos_csv(ARCHIVO)
else:
    print(f"📂 Archivo existente encontrado: {ARCHIVO}")

# Simula envío periódico (3 ciclos con espera de 2 segundos)
for i in range(3):
    print(f"\n🚀 Iteración {i+1}: leyendo y actualizando datos...")
    procesar_y_actualizar_archivo(ARCHIVO)
    print("⏳ Esperando 5 minutos (simulado con 2 segundos)...\n")
    time.sleep(2)

print("🎯 Simulación completa.")