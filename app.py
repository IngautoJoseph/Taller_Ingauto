import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

# Crear carpeta de reportes si no existe
if not os.path.exists("reportes"):
    os.makedirs("reportes")

st.set_page_config(page_title="Registro de Citas - Ingauto", layout="centered")
st.title("📋 Registro de Citas - Ingauto Catamayo")

st.subheader("Datos del Cliente")
nombre = st.text_input("Nombre completo")
telefono = st.text_input("Número de teléfono")
cedula_ruc = st.text_input("RUC o cédula")

st.subheader("Datos del Vehículo")
marca = st.text_input("Marca")
modelo = st.text_input("Modelo")
ano = st.text_input("Año")
placa = st.text_input("Placa")
kilometraje = st.text_input("Kilometraje")
combustible = st.selectbox("Tipo de combustible", ["Gasolina", "Diésel"])
motor = st.text_input("Número de motor")
chasis = st.text_input("Número de chasis")

st.subheader("Servicio Solicitado")
mantenimientos = [
    "Mantenimiento de 5.000 km",
    "Mantenimiento de 7.500 km",
    "Mantenimiento de 10.000 km",
    "Mantenimiento de 15.000 km",
    "Mantenimiento de 20.000 km",
    "Mantenimiento de 25.000 km",
    "Mantenimiento de 30.000 km",
    "Mantenimiento de +30.000 km"
]
servicio = st.selectbox("Selecciona el servicio", mantenimientos)
otro_servicio = st.text_input("Otro servicio adicional (opcional)")
observaciones = st.text_area("Observaciones (opcional)")

st.subheader("Información de la Cita")
fecha_cita = st.date_input("Fecha de la cita")
hora_cita = st.time_input("Hora estimada")

if st.button("Registrar y generar PDF"):
    datos = {
        "Fecha de registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nombre": nombre,
        "Teléfono": telefono,
        "RUC/Cédula": cedula_ruc,
        "Marca": marca,
        "Modelo": modelo,
        "Año": ano,
        "Placa": placa,
        "Kilometraje": kilometraje,
        "Combustible": combustible,
        "Motor": motor,
        "Chasis": chasis,
        "Servicio": servicio,
        "Otro servicio": otro_servicio,
        "Observaciones": observaciones,
        "Fecha cita": fecha_cita.strftime("%Y-%m-%d"),
        "Hora cita": hora_cita.strftime("%H:%M")
    }

    # Guardar en CSV
    df = pd.DataFrame([datos])
    if os.path.exists("citas.csv"):
        df.to_csv("citas.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("citas.csv", index=False)

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="CITA TALLER - INGAUTO CATAMAYO", ln=True, align='C')
    pdf.ln(10)
    for key, value in datos.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    nombre_archivo = f"reportes/Cita_{nombre.replace(' ', '_')}_{placa}.pdf"
    pdf.output(nombre_archivo)

    st.success("✅ Cita registrada correctamente.")
    st.info(f"📄 PDF generado: {nombre_archivo}")
