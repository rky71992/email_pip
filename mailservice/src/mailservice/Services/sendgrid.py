#!/usr/bin/python3

import pydantic
from definations import (DeliveryStandardResponse, DeliveryStatus)
#from MailService import (DeliveryStandardResponse, DeliveryStatus)
#from MailService
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendgridAddService(pydantic.BaseModel):
    '''Model for keys required to Sendgrid service to mailing services'''
    key: str
    service_name: str = "sendgrid"

    @pydantic.validator("key")
    @classmethod
    def key_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError("Key cannot be empty")
        return value.strip()


class SendgridMailService:
    SERVICE_NAME = "sendgrid"
    def __init__(self) -> None:
        self.response = {}
        self.response["service_name"] = SendgridMailService.SERVICE_NAME
        self.response["api_status_code"] = 200
        self.response["error"] = ""
        
    def send_mail(self, service_details: SendgridAddService, recipitent: str ,mail: Mail ) -> DeliveryStandardResponse:
        self.response["recipitent"] = recipitent
        self.response["sender"] = mail.sender

        message = Mail(
            from_email=mail.sender,
            to_emails=recipitent,
            subject=mail.subject,
            html_content=mail.text)
        try:
            sg = SendGridAPIClient(service_details.key)
            res = sg.send(message)
        except Exception as e:
            self.response["delivery_status"] = DeliveryStatus.FAILED
            self.response["error"] = str(e)
        else:
            try:
                if res.status_code == 200:
                    self.response["delivery_status"] = DeliveryStatus.SUCCESS
                else:
                    self.response["delivery_status"] = DeliveryStatus.FAILED
            except Exception:
                self.response["delivery_status"] = DeliveryStatus.FAILED
            
        
        return DeliveryStandardResponse(**self.response).model_dump()