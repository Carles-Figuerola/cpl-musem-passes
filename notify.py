import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Notify():
    def __init__(self, config):
        self.config = config
            
        
    def send_email(self, subject, html_content):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f'CPL Museum Passes <{self.config["from"]}>'
        message["To"] = ",".join(self.config["to"])
        html = MIMEText(html_content, "html")
        message.attach(html)

        with smtplib.SMTP_SSL(self.config["smtp"], self.config["port"]) as server:
            server.ehlo()
            server.login(self.config["username"], self.config["password"])
            result = server.sendmail(self.config["from"], self.config["to"], message.as_string())

        if len(result) > 0:
            return result
        
        return True
