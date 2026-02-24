import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "auth.plataforma.online@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "tpmi yzlw raex dcos")

def send_email(target_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = target_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, target_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

def send_otp_email(target_email: str, otp: str):
    subject = "Seu Código de Acesso"
    body = f"Seu código de acesso de 4 dígitos é: {otp}\nEle expira em 10 minutos."
    return send_email(target_email, subject, body)

def send_reset_email(target_email: str, token: str):
    subject = "Recuperação de Senha"
    body = f"Use o seguinte token para resetar sua senha: {token}\nEle expira em 1 hora."
    return send_email(target_email, subject, body)
