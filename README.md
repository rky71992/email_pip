# Mail Service

A simple service to send mail.

## Installation



## A Simple Example

```py
from MailService import MailService
a = MailService()
a.add_services([{"id":"sendgrid","key":"some_key"}])
a.add_mail({"sender":"rky71992@gmail.com","recievers":["test@gmail.com"],"subject":"This is the mail sub","text":"some text ti send"})
x = a.send_mail()
print(x)
```
