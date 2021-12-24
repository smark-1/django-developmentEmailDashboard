from django.db import models
from django.urls import reverse, NoReverseMatch, get_script_prefix
from django.utils.encoding import iri_to_uri

# model for each email account with the email address
class Inbox(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.email

    def get_unread_email_number(self):

        return InboxEmail.objects.filter(inbox=self,read=False).count()

    def get_absolute_url(self):
        try:
            return reverse('developmentEmailDashboard:inbox_view', kwargs={'email': self.email})
        except NoReverseMatch:
            pass
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix().rstrip('/') + self.url)

# model for the actual email message
class DevelopmentEmail(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    from_email=models.EmailField()
    extra_headers = models.JSONField()
    to = models.JSONField()
    bcc = models.JSONField()
    cc = models.JSONField()
    reply_to = models.JSONField()
    email_type = models.CharField(max_length=20)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'from: {self.from_email} |  {self.subject[:20]}...'


# model for the unique email the user deletes/reads/sends etc
class InboxEmail(models.Model):
    inbox = models.ForeignKey(Inbox,on_delete=models.CASCADE)
    email = models.ForeignKey(DevelopmentEmail,on_delete=models.CASCADE)

    read = models.BooleanField(default=False)
    is_sender = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']


