import smtplib
from email.mime.text import MIMEText

def send_email(to_email,pwd):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.set_debuglevel(1)
    smtp.ehlo("gmail.com")
    smtp.login(user = 'gjihun852@gmail.com', password='poqgkvcbrzaznlwp')
    html_message = """
        <html>
        <head></head>
        <body>
            <p>청취자들의 임시 비밀번호 입니다.</p>
            <p>
        """ + pwd + """
    
            </p>
        </body>
        </html>
    """
    msg = MIMEText(html_message,"html")
    msg['Subject'] = '청취자들 임시 비밀번호 발급 안내'

    smtp.sendmail(from_addr='gjihun852@gmail.com', to_addrs =to_email, msg =msg.as_string())

    smtp.quit()
