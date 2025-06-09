
import streamlit as st
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

# Función para generar el PDF
def generar_pdf(datos, nombre_archivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for clave, valor in datos.items():
        pdf.cell(200, 10, txt=f"{clave}: {valor}", ln=True)
    pdf.output(nombre_archivo)

# Función para enviar el PDF por correo
def enviar_pdf_por_correo(remitente, clave, destinatario, archivo, asunto):
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario
    msg.set_content("Adjunto encontrarás la cita generada en PDF.")

    with open(archivo, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(archivo)
    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, clave)
        smtp.send_message(msg)

# Streamlit UI
st.title("Sistema de Citas - Ingauto Catamayo")

with st.form("formulario_cita"):
    nombre = st.text_input("Nombre completo")
    telefono = st.text_input("Teléfono")
    cedula = st.text_input("Cédula / RUC")
    correo_cliente = st.text_input("Correo del cliente")
    marca = st.text_input("Marca del vehículo")
    modelo = st.text_input("Modelo")
    anio = st.text_input("Año")
    placa = st.text_input("Placa")
    kilometraje = st.text_input("Kilometraje")
    combustible = st.selectbox("Combustible", ["Gasolina", "Diésel"])
    motor = st.text_input("Motor")
    chasis = st.text_input("Chasis")
    servicio = st.selectbox("Servicio solicitado", ["Mantenimiento de 5000 km", "Mantenimiento de 10000 km", "Mantenimiento de 15000 km"])
    fecha = st.date_input("Fecha de cita")
    hora = st.time_input("Hora")
    enviar = st.form_submit_button("Registrar y generar PDF")

if enviar:
    datos = {
        "Nombre": nombre,
        "Teléfono": telefono,
        "Cédula / RUC": cedula,
        "Correo": correo_cliente,
        "Marca": marca,
        "Modelo": modelo,
        "Año": anio,
        "Placa": placa,
        "Kilometraje": kilometraje,
        "Combustible": combustible,
        "Motor": motor,
        "Chasis": chasis,
        "Servicio solicitado": servicio,
        "Fecha de cita": str(fecha),
        "Hora": str(hora),
    }

    nombre_pdf = f"cita_{placa}_{fecha}.pdf"
    ruta_pdf = os.path.join("/tmp", nombre_pdf)
    generar_pdf(datos, ruta_pdf)

    st.success("✅ Cita registrada correctamente.")
    with open(ruta_pdf, "rb") as f:
        st.download_button("⬇️ Descargar PDF", data=f, file_name=nombre_pdf, mime="application/pdf")

    # Enviar el PDF al correo del cliente y al correo del taller
    try:
        remitente = "accesoriossd@ingauto.com.ec"
        clave_app = "51TBdC375q"
        enviar_pdf_por_correo(remitente, clave_app, correo_cliente, ruta_pdf, "Tu cita en Ingauto")
        enviar_pdf_por_correo(remitente, clave_app, "accesoriossd@ingauto.com.ec", ruta_pdf, "Nueva cita registrada")
        st.info("📧 PDF enviado correctamente a ambos correos.")
    except Exception as e:
        st.error(f"Error al enviar correo: {e}")
