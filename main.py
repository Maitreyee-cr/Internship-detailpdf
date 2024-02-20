from flask import Flask, render_template, request
from jinja2 import Template
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

def create_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    # Insert data into PDF
    c.drawString(100, 750, "Email: " + data['email'])
    c.drawString(100, 730, "Name: " + data['name'])
    c.drawString(100, 710, "Start Date: " + data['start_date'])
    c.drawString(100, 690, "End Date: " + data['end_date'])
    c.save()

def send_email_attachment(To, subject, message, data):
    msg = MIMEMultipart()
    sender = 'iammaitreyee1@gmail.com'
    msg['From'] = sender
    msg['To'] = To
    msg['Subject'] = subject
    file_name = To + '.pdf'
    create_pdf(data, file_name)
    msg.attach(MIMEText(message))
    filename = file_name
    path = os.path.join(os.getcwd(), filename)
    with open(path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'Enter the email'
    smtp_password = 'Enter your pasword'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, To, msg.as_string())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        data = {
            'email': email,
            'name': name,
            'start_date': start_date,
            'end_date': end_date
        }
        send_email_attachment(email, 'Your PDF Attachment', 'Please find attached PDF', data)
        return 'Email sent successfully!'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
