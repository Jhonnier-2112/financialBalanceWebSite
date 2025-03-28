from flask_mail import Message
from flask import render_template, current_app
from config.extensions import mail
import os


def send_email(to, name, new_password):
    subject = "🔐 Restablecimiento de Contraseña"
    sender = current_app.config["MAIL_USERNAME"]

    print("Current working directory:", os.getcwd())  # Verifica en qué carpeta está Flask
    print("Template path:", os.path.exists("templates/email/reset_password.html"))
    # Renderizar la plantilla con los datos del usuario
    html_body = render_template("email/reset_password.html", name=name, new_password=new_password)

    msg = Message(subject, sender=sender, recipients=[to])
    msg.html = html_body  # 📩 Enviar en formato HTML

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False
