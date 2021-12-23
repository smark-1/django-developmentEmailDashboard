from django.core.mail.backends.base import BaseEmailBackend
from .models import DevelopmentEmail,Inbox,InboxEmail

class developmentEmailBackend(BaseEmailBackend):
    def send_messages(self,email_messages):
        for email in email_messages:
            devemail = DevelopmentEmail.objects.create(subject=email.subject,body=email.body,
                                                       from_email=email.from_email,extra_headers=email.extra_headers,
                                                       to=email.to,bcc=email.bcc,cc=email.cc,reply_to=email.reply_to)

            # add email to senders outbox
            inbox, created = Inbox.objects.get_or_create(email=email.from_email)
            InboxEmail.objects.create(inbox=inbox, email=devemail,is_sender=True)


            # add email to to inbox
            for email_address in email.to:
                self.send_email(devemail,email_address)

            # add email to bcc inbox
            for email_address in email.bcc:
                self.send_email(devemail, email_address)

            # add email to cc inbox
            for email_address in email.cc:
                self.send_email(devemail, email_address)

        return len(email_messages)


    def send_email(self,email,emailAddress):
        inbox, created = Inbox.objects.get_or_create(email=emailAddress)
        InboxEmail.objects.create(inbox=inbox, email=email)
