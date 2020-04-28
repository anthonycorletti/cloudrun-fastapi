import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To

from config import apisecrets

sg = sendgrid.SendGridAPIClient(api_key=apisecrets.SENDGRID_API_KEY)


def send(from_email: str, to_email: str, subject: str, mime_type: str,
         content: str):
    from_email = Email(from_email)
    to_email = To(to_email)
    subject = "Sending with SendGrid is Fun"
    content = Content(mime_type, content)
    mail = Mail(from_email, to_email, subject, content)

    response = sg.client.mail.send.post(request_body=mail.get())

    return response
