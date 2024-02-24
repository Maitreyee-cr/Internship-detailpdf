from flask import Flask, render_template, request
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import pdfkit


app = Flask(__name__)

wkhtml_path = pdfkit.configuration(wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")  #by using configuration you can add path value.


def create_pdf(data, filename):
    # Load the Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))
    
    # Render the HTML template with the provided data
    template = env.get_template('templates/newpdf.html')
    html_content = template.render(email=data['email'], name=data['name'], 
                           start_date=data['start_date'], end_date=data['end_date'])
    print (html_content)
    # Convert HTML to PDF
    pdfkit.from_string(html_content, filename, configuration=wkhtml_path)
    
    
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
    smtp_username = 'enter you email'
    smtp_password = 'enter app-password'

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
@app.route('/pdf',methods=['GET'])
def pdfmaker():
    return render_template('newpdf.html',email='abc@gmail.com',name='abc',start_date='2024-02-06', end_date='2024-05-06')
if __name__ == '__main__':
    app.run(debug=True)
