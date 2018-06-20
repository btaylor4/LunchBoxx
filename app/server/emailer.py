import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("the.ultislackers@gmail.com", "iloveslacking")

msg = MIMEMultipart()
msg['From'] = "the.ultislackers@gmail.com"
msg['To'] = "clearly.b.t@gmail.com"
msg['Subject'] = "Your lunchboxx is ready!"
body = "Here are your lunchboxx details! You will be eating at Tearentella at 12:00 PM. Enjoy your lunch!"
msg.attach(MIMEText(body, 'plain'))

server.sendmail("the.ultislackers@gmail.com",
                "clearly.b.t@gmail.com", msg.as_string())
server.quit()
