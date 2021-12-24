from django.core.mail.backends.base import BaseEmailBackend
from .models import DevelopmentEmail, Inbox, InboxEmail
from django.conf import settings
import webbrowser
notification_callback_ids = {}


class developmentEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for email in email_messages:
            devemail = DevelopmentEmail.objects.create(subject=email.subject, body=email.body,
                                                       email_type=email.content_subtype,
                                                       from_email=email.from_email, extra_headers=email.extra_headers,
                                                       to=email.to, bcc=email.bcc, cc=email.cc, reply_to=email.reply_to)

            # add email to senders outbox
            inbox, created = Inbox.objects.get_or_create(email=email.from_email)
            InboxEmail.objects.create(inbox=inbox, email=devemail, is_sender=True,read=True)

            # add email to to inbox
            for email_address in email.to:
                self.send_email(devemail, email_address)

            # add email to bcc inbox
            for email_address in email.bcc:
                self.send_email(devemail, email_address)

            # add email to cc inbox
            for email_address in email.cc:
                self.send_email(devemail, email_address)

        return len(email_messages)

    def send_email(self, email, emailAddress):
        inbox, created = Inbox.objects.get_or_create(email=emailAddress)
        InboxEmail.objects.create(inbox=inbox, email=email)

        # send a windows notification if send email notification is set to true
        try:
            if settings.DEVELOPMENT_EMAIL_DASHBOARD_SEND_EMAIL_NOTIFICATION:
                send_notification(email, inbox)
        except AttributeError:
            pass


def notificationClickHandler(notification_id):
    url = notification_callback_ids[notification_id]
    webbrowser.open(f'http://localhost:8000{url}')



def send_notification(email, inbox):
    try:
        import zroya

        # send notification
        zroya.init("django-developmentEmailDashboard", "dragoncommits",
                   'django-developmentEmailDashboard', 'django-developmentEmailDashboard', '1')
        t = zroya.Template(zroya.TemplateType.Text2)

        t.setFirstLine(f'"{inbox.email}" received a new email')
        t.setSecondLine(email.subject)
        id = zroya.show(t, on_click=notificationClickHandler)
        notification_callback_ids[id] = inbox.get_absolute_url()

    except ModuleNotFoundError:
        print(
            'to show notifications about receiving emails you must install zroya first install zroya | pip install zroya')
