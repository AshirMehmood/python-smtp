"""
Defining an SMPT automating script, that can send customized emails, to recipients defined in a
csv file, we require user name and password, the password must not be hardcoded, rather used as
a env variable
"""
import smtplib
from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import csv
# multipurpose internet mail extension

email = config("my_email")
password = config("password")

gmail_server = "smtp.gmail.com"
port = 587


my_server  = smtplib.SMTP(gmail_server, port)
my_server.ehlo()
my_server.starttls

my_server.login(email, password)

message = MIMEMultipart("alternative")
text = "your_message"
message.attach(MIMEText(text))

my_image = "/path/img.jpg"
image = open(my_image, 'rb').read()

message.attach(MIMEImage(image, name=os.path.basename(my_image)))

# attaching files
file_path = "./file.ext"

with open(file_path, 'rb') as f:
    file = MIMEApplication(
        f.read(),
        name=os.path.basename(file_path)
    )
    file['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    message.attach(file)

    with open("file.csv") as csv_file:
        jobs = csv.reader(csv_file)
        next(jobs)

        for rec_name, rec_email, org, sector, role in jobs:
            email_text=text.format(rec_name, rec_email, org, sector, role)
            message.attach(MIMEText(email_text))

            my_server.sendmail(
                from_addr=email,
                to_addrs=rec_email,
                msg=message
            )
            
my_server.quit()