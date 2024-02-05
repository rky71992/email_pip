#!/usr/bin/python3

import pydantic
from definations import (DeliveryStandardResponse, DeliveryStatus,
                         MailServiceMail)

import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError


class MailChimpAddService(pydantic.BaseModel):
    '''Model for keys required to add Mailchimp service to mailing services'''
    key: str
    service_name: str = "mailchimp"

    @pydantic.validator("key")
    @classmethod
    def key_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError("Key cannot be empty")
        return value.strip()


class MailChimpMailService:
    '''Class to process and send mail using MailChimp'''
    SERVICE_NAME = "mailchimp"
    def __init__(self) -> None:
        self.response = {}
        self.response["service_name"] = MailChimpMailService.SERVICE_NAME
        self.response["api_status_code"] = 200
        self.response["error"] = ""
        
    def send_mail(self, service_details: MailChimpAddService, recipitent: str ,mail: MailServiceMail ) -> DeliveryStandardResponse:
        '''send mail to recipitent using mailgun pip package'''
        self.response["recipitent"] = recipitent
        self.response["sender"] = mail.sender

        mailchimp = MailchimpTransactional.Client(service_details.key)
        message = {
                "from_email": mail.sender,
                "subject": mail.subject,
                "text": mail.text,
                "to": [
                {
                    "email": recipitent,
                    "type": "to"
                }
                ]
            }
        try:
            res = mailchimp.messages.send({"message":message})
            self.response["delivery_status"] = DeliveryStatus.SUCCESS
        except ApiClientError as error:
            self.response["delivery_status"] = DeliveryStatus.FAILED
            self.response["error"] = str(error.text)    
        
        return DeliveryStandardResponse(**self.response)