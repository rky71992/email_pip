

import pydantic
from email_validator import validate_email
from typing import Optional
from dataclasses import dataclass


@dataclass
class DeliveryStatus:
    SUCCESS: str = "success"
    FAILED: str = "failed"


class MailServiceMail(pydantic.BaseModel):
    sender: str
    recievers: list 
    subject: str
    text : str

    @pydantic.validator("sender")
    @classmethod
    def sender_validator(cls, value) -> str:
        email_info = validate_email(value, check_deliverability=False)
        return email_info.normalized
    
    @pydantic.validator("recievers")
    @classmethod
    def recievers_validator(cls, value) -> list:
        normalized_emails: list = []
        for r_email in value:
            email_info = validate_email(r_email, check_deliverability=False)
            normalized_emails.append(email_info.normalized)
        return normalized_emails
    
    @pydantic.validator("subject")
    @classmethod
    def subject_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError("Subject cannot be empty")
        return value.strip()

    @pydantic.validator("text")
    @classmethod
    def text_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError("Message cannot be empty")
        return value.strip()
    

class DeliveryStandardResponse(pydantic.BaseModel):
    '''Standard response which each service should return when calling send_mail'''
    service_name: str
    delivery_status: str
    error: Optional[str] = ""
    sender: str
    recipitent: str


class MailServiceStandardResponse(pydantic.BaseModel):
    '''Response which MailService will return'''
    sender: str
    subject: str
    text: str
    recipitents: list
