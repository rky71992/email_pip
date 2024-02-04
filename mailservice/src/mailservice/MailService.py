#!/usr/bin/python3

from Services.sendgrid import SendgridAddService, SendgridMailService
from definations import (MailServiceMail, MailServiceStandardResponse,
                         DeliveryStandardResponse, DeliveryStatus)


class MailService(object):
    '''Sends mail using different services from SUPPORTED_SERVICES'''
    SENDGRID = "sendgrid"
    MAILGUN= "mailgun"
    MANDRIL = "mandril"
    SUPPORTED_SERVICES = [SENDGRID, MAILGUN, MANDRIL]
    
    
    def __init__(self) -> None:
        self.mail: MailServiceMail = None
        self.mail_services: list = []
        self.service_processed: bool = False


    def __add_services_mapper(self,service_name):
        MAPPER = {
            MailService.SENDGRID: SendgridAddService,
            #MailService.MAILGUN: 
            #MailService.MANDRIL:
        }
        return MAPPER[service_name]
    

    def __send_mail_service_mapper(self, service_name:str):
        MAPPER = {
            MailService.SENDGRID : SendgridMailService,
            #MailService.MAILGUN : MailgunMailService,
            #MailService.MANDRIL : MandrilMailService
        }
        return MAPPER[service_name]()
        
    
    def add_services(self, services_list: list) -> None:
        '''Add requested services which are in SUPPORTED_SERVICES for mailing'''
        if not isinstance(services_list,list):
            raise TypeError(f"add_service accepts list containg services dict. Invalid argument passed: {type(services_list)}")
        
        for service in services_list:
            if not isinstance(service,dict):
                raise TypeError(f"Service is of type dict expected. Invalid argument passed:{type(service)}")
            if service.get("id","").strip().lower() not in MailService.SUPPORTED_SERVICES:
                raise ValueError(f"Service not supported: {service.get('id')}")
            
            self.mail_services.append(self.__add_services_mapper(service.get("id","").strip().lower())(**service))

    
    def add_mail(self, mail_block_dict: dict) -> None:
        '''Add MailServiceMail model instance
        mail_block_dict = {
        "sender":"abc@gmail.com",
        "recievers":["xyz@gg.com","akf@kk.org"],
        "subject":"some test subject",
        "text":"text to send"
        }
        '''
        self.mail = MailServiceMail(**mail_block_dict)
    

    def send_mail(self) -> MailServiceStandardResponse:
        '''Sends mail to each recipitent using different services'''
        if self.service_processed:
            raise Exception("Mail service already called. Cannot call again.")
        
        return_dict = self.mail.model_dump(include=["sender","subject","text"])
        recipitent_delivery_reponses = []
        for recipitent in self.mail.recievers:
            recepitent_responses = []
            for delivery_service in self.mail_services:
                ms = self.__send_mail_service_mapper(delivery_service.service_name)
                response: DeliveryStandardResponse = ms.send_mail(delivery_service,recipitent,self.mail)
                recepitent_responses.append(response.model_dump(exclude=["recipitent","sender"]))
                if response.delivery_status == DeliveryStatus.SUCCESS:
                    break
            recipitent_delivery_reponses.append({"recipitent":recipitent, "service_delivery":recepitent_responses})

        return_dict["recipitents"] = recipitent_delivery_reponses

        return MailServiceStandardResponse(**return_dict).model_dump()


