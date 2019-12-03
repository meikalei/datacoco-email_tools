import unittest
from unittest.mock import patch
from datacoco_email_tools import Email


class TestEmail(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.email = Email()
        cls.expected_response = {"MessageId": "string"}

    @patch("datacoco_email_tools.email_tools.Email.send_email_with_attachment")
    def test_send_email_with_attachment(self, mock_send_email_with_attachment):
        print("--------------test_send_email_with_attachment")

        mock_send_email_with_attachment.return_value = self.expected_response

        response = self.email.send_email_with_attachment(
            aws_access_key="aws_access_key",
            aws_secret_key="aws_secret_key",
            aws_sender="aws_sender",
            aws_region="aws_region",
            to_addr="email@email.com",
            subject="hello world",
            from_addr="email@gmail.com",
            filename="helloworld.txt",
            body_msg="email body text",
        )

        self.assertDictEqual(response, self.expected_response)

    @patch("datacoco_email_tools.email_tools.Email.send_mail")
    def test_send_mail(self, mock_send_mail):
        print("--------------test_send_mail")

        mock_send_mail.return_value = self.expected_response

        response = self.email.send_mail(
            aws_access_key="aws_access_key",
            aws_secret_key="aws_secret_key",
            aws_sender="aws_sender",
            aws_region="aws_region",
            to_addr="email@email.com",
            subject="hello world",
            from_addr="email@gmail.com",
            text_msg="text message",
        )

        self.assertDictEqual(response, self.expected_response)
