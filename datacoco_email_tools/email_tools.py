"""
Generic email module
"""
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3


class Email:
    """
    Send emails via Amazon Simple Email Service (SES)
    """

    def __init__(
        self,
        recipients=None,
        subject=None,
        cc_recipients=None,
        bcc_recipients=None,
        aws_access_key=None,
        aws_secret_key=None,
        aws_sender=None,
        aws_region=None,
    ):
        """
        :param recipients: email 'To:', [list of email recipients]
        :param subject:
        :return:
        """
        self.to = recipients
        self.cc = cc_recipients
        self.bcc = bcc_recipients
        self.subject = subject
        self._html = ""
        self._text = ""
        self._aws_access_key = aws_access_key
        self._aws_secret_key = aws_secret_key
        self._aws_sender = aws_sender
        self._aws_region = aws_region

    def html(self, html=""):
        """
        Sets email html message property
        :param html:
        :return:
        """
        self._html = html
        self._email_body = {"Html": {"Charset": "UTF-8", "Data": self._html,}}

    def text(self, text=""):
        """
        Sets email text message property
        :param text:
        :return:
        """
        self._text = text
        self._email_body = {"Text": {"Charset": "UTF-8", "Data": self._text,}}

    def connect_to_email_client(self):
        """
        Connect to AWS SES client
        """
        try:
            self.client = boto3.client(
                "ses",
                region_name=self._aws_region,
                aws_access_key_id=self._aws_access_key,
                aws_secret_access_key=self._aws_secret_key,
            )
            print("Connected to SES client")
        except Exception as e:
            raise e

    def create_attachment(
        self,
        body_msg,
        filename,
        file_string=None,
        from_addr=None,
        filepath=None,
    ):
        """
        Build raw email message for attachment
        :param body_msg:
        :param filename:
        :param from_addr:
        """
        if not from_addr:
            from_addr = self._aws_sender

        self._attachment_msg = MIMEMultipart()
        self._attachment_msg["Subject"] = self.subject
        self._attachment_msg["From"] = from_addr
        # needed if there are multiple recipients
        self._attachment_msg["To"] = ", ".join(self.to)
        if self.cc:
            self._attachment_msg["Cc"] = self.cc
        if self.bcc:
            self._attachment_msg["Bcc"] = self.bcc

        # the message body
        part = MIMEText(body_msg, "html")

        self._attachment_msg.attach(part)

        # the attachment
        if file_string:
            part = MIMEApplication(str.encode(file_string))
        else:
            # backward compatibility
            path = filepath if filepath else filename
            part = MIMEApplication(open(path, "rb").read())

        part.add_header("Content-Disposition", "attachment", filename=filename)
        self._attachment_msg.attach(part)

    def send(self, from_addr=None):
        """
        Sends email
        :param from_addr:
        :return:
        """
        if isinstance(self.to, str):
            self.to = [self.to]
        if not from_addr:
            from_addr = self._aws_sender
        if not self._html and not self._text:
            raise Exception("You must provide a text or html body.")

        self.connect_to_email_client()

        response = self.client.send_email(
            Destination={"ToAddresses": self.to},
            Message={
                "Body": self._email_body,
                "Subject": {"Charset": "UTF-8", "Data": self.subject,},
            },
            Source=from_addr,
        )

        print("Email sent")

        return response

    def send_attachment(self, from_addr=None):
        """
        Sends attachment email
        :param from_addr:
        :return:
        """
        if not from_addr:
            from_addr = self._aws_sender

        self.connect_to_email_client()

        send_attachment_args = {
            "Source": from_addr,
            "Destinations": self.to,
            "RawMessage": {"Data": self._attachment_msg.as_string()},
        }

        if self.bcc or self.cc:
            # Need to remove Destinations arg to allow for cc or bcc recipients
            send_attachment_args.pop("Destinations")

        response = self.client.send_raw_email(**send_attachment_args)

        print("Email with attachment sent")

        return response

    @staticmethod
    def send_email_with_attachment(
        to_addr,
        subject,
        body_msg,
        filename,
        aws_access_key=None,
        aws_secret_key=None,
        aws_sender=None,
        file_string=None,
        aws_region=None,
        from_addr=None,
        cc_recipients=None,
        bcc_recipients=None,
        filepath=None,
    ):
        """
        Simple one line wrapper for Email class with attachment
        :param aws_access_key:
        :param aws_secret_key:
        :param aws_sender:
        :param to_addr:
        :param subject:
        :param filename:
        :param body_msg:
        :param aws_region:
        :param from_addr:
        :return:
        """
        email = Email(
            recipients=to_addr,
            subject=subject,
            cc_recipients=cc_recipients,
            bcc_recipients=bcc_recipients,
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            aws_sender=aws_sender,
            aws_region=aws_region,
        )
        email.create_attachment(
            body_msg, filename, file_string, from_addr, filepath
        )
        return email.send_attachment(from_addr)

    @staticmethod
    def send_mail(
        to_addr,
        subject,
        aws_access_key=None,
        aws_secret_key=None,
        aws_sender=None,
        aws_region=None,
        from_addr=None,
        text_msg="",
        html_msg="",
    ):
        """
        Simple one line wrapper for Email class
        :param aws_access_key:
        :param aws_secret_key:
        :param aws_sender:
        :param to_addr:
        :param subject:
        :param aws_region:
        :param from_addr:
        :param text_msg:
        :param html_msg:
        :return:
        """
        email = Email(
            recipients=to_addr,
            subject=subject,
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            aws_sender=aws_sender,
            aws_region=aws_region,
        )
        if html_msg:
            email.html(html_msg)
        elif text_msg:
            email.text(text_msg)
        return email.send(from_addr)
