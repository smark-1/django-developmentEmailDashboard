from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import InboxEmail


@receiver(post_delete, sender=InboxEmail)
def delete_development_email_if_nothing_attached(sender, instance, using, **kwargs):
    # get the models.DevelopmentEmail from the models.InboxEmail
    try:
        developmentEmail = instance.email

        # get all the InboxEmails associated with the parent email (models.DevelopmentEmail)
        emails = InboxEmail.objects.filter(email=developmentEmail)

        # only delete the DevelopmentEmail object if no InboxEmails refer to it
        if not emails.exists():

            developmentEmail.delete()

    except Exception as e:
        print(e)
