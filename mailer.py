import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

root_email = 'dentalinformationsystem@gmail.com'
email_password = 'hapusvsyzzdtgagj'
def establish_smtp_connection():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(root_email, email_password)
    return server


def sendMessage(patient, date, time):
    server = establish_smtp_connection()

    message = MIMEMultipart()
    message["From"] = root_email
    message["To"] = patient.email
    message["Subject"] = 'Confirmation of Appointment, request by ' + patient.firstname + ' ' + patient.lastname
    body_message = f"""
                        Dear {patient.firstname},

                        I hope this message finds you well. We appreciate your recent appointment request, and I'm pleased to inform you that we have successfully verified and scheduled the appointment with our dentist.

                        Your preferred date and time have been reserved, and we look forward to providing you with excellent dental care on {date} at {time}. Our team is committed to ensuring a comfortable and efficient experience during your visit.

                        If you have any specific concerns or additional requests, please feel free to let us know in advance, and we will do our best to accommodate them.

                        Thank you for choosing our dental services. We value your trust and are dedicated to delivering the highest quality care. If you have any questions or need further assistance, please don't hesitate to contact us.

                        We look forward to seeing you soon!

                        Best regards,

                        {patient.firstname}, {patient.lastname}
                        dentalinformationsystem@gmail.com
                    """
    message.attach(MIMEText(body_message, "plain"))

    server.send_message(message)
    server.quit()
