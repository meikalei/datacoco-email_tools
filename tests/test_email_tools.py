import unittest

from datacoco_email_tools import Email


class TestEmail(unittest.TestCase):
    def test_email(self):
        print("--------------test_email")

        AWS_ACCESS_KEY = "aws_access_key"
        AWS_SECRET_KEY = "aws_secret_key"
        SENDER = "sender"
        AWS_REGION = "aws_region"
        RECIPIENTS = "email@gmail.com"

        Email.send_mail(
            aws_access_key=AWS_ACCESS_KEY,
            aws_secret_key=AWS_SECRET_KEY,
            aws_sender=SENDER,
            aws_region=AWS_REGION,
            to_addr=RECIPIENTS,
            subject="hello world",
            from_addr="email@gmail.com",
            text_msg="text message",
            html_msg="html message",
        )

        Email.send_email_with_attachment(
            aws_access_key=AWS_ACCESS_KEY,
            aws_secret_key=AWS_SECRET_KEY,
            aws_sender=SENDER,
            to_addr=RECIPIENTS,
            subject="hello world",
            from_addr="email@gmail.com",
            filename="helloworld.txt",
            aws_region=AWS_REGION,
            body_msg="email body text",
        )
