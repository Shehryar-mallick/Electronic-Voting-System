import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


mail_content = '''Hello,
Hope to find you in a pleasant state.
In this mail we are sending the voting statistics.
Do not reply to this email.
Thank You
'''

# The mail addresses and password
sender_address = 'sskenterprises486@gmail.com'
sender_pass = 'unimaginable_TRUE_4_'
# receiver_address_list = ['user1@gmail.com', 'user2@gmail.com', 'user3@gmail.com', 'user4@gmail.com']


# def add_mail(mail):
#     receiver_address_list.append(mail)
#

def send_mail(receiver_address_list):
    for i in range(len(receiver_address_list)):
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address_list[i]
        message['Subject'] = 'It has an important attachment.'
        # The subject line

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        attach_file_name = 'DetailedReport.pdf'
        attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
        payload = MIMEBase('application', 'pdf', Name=attach_file_name)
        payload.set_payload(attach_file.read())
        encoders.encode_base64(payload)  # encode the attachment
        # add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', Name=attach_file_name)
        message.attach(payload)
        print(attach_file_name)
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address_list[i], text)
        session.quit()
        print('Mail Sent')
