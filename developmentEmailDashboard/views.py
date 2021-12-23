from django.core.mail import send_mail
import json

from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Inbox, DevelopmentEmail, InboxEmail
from django.db.models import Count
from django.contrib import messages
from django.views.decorators.clickjacking import xframe_options_sameorigin


# Create your views here.

def inboxesView(request):
    # display all the inboxes
    inboxes = Inbox.objects.all().annotate(Count('inboxemail')).order_by('-created')
    return render(request, 'developmentEmailDashboard/inboxesView.html', context={'inboxes': inboxes})


def inboxView(request, email):
    # display all sent and received emails for specific inbox
    inbox = get_object_or_404(Inbox, email=email)
    emails = InboxEmail.objects.filter(inbox=inbox, is_sender=False).order_by('-created')
    sentEmails = InboxEmail.objects.filter(inbox=inbox, is_sender=True).order_by('-created')
    return render(request, 'developmentEmailDashboard/inboxView.html', context={'inbox': inbox,
                                                                                'emails': emails,
                                                                                'sentEmails': sentEmails})


@xframe_options_sameorigin
def emailView(request, email, id):
    # displays actual email in a iframe
    inbox = get_object_or_404(Inbox, email=email)
    inboxes = Inbox.objects.all()
    email = get_object_or_404(InboxEmail, inbox=inbox, id=id)
    email.read = True
    email.save()
    return render(request, 'developmentEmailDashboard/emailView.html',
                  context={'inbox': inbox, 'email': email, 'inboxes': inboxes})


def replyEmail(request, email, id):
    # this email-backend does not support any replying to capability, so it
    # sends email with same subject to reply_to field

    inbox = get_object_or_404(Inbox, email=email)
    inboxemail = get_object_or_404(InboxEmail, inbox=inbox, id=id)

    toemails = []
    for em in json.loads(request.POST.get('reply_to')):
        toemails.append(em['tag'])
    send_mail(
        inboxemail.email.subject,
        request.POST.get('content', ''),
        request.POST.get('from_address', ''),
        toemails,
        fail_silently=False,
    )
    messages.info(request, f'sent reply to {toemails}')
    return redirect(reverse('developmentEmailDashboard:email_view', args=(email, id)))


def deleteEmail(request, email, id):
    # deletes the email for specified inbox if no other inboxes have this email
    # will delete models.DevelopmentEmail instance of it
    inbox = get_object_or_404(Inbox, email=email)
    inboxemail = get_object_or_404(InboxEmail, inbox=inbox, id=id)
    inboxemail.delete()
    messages.info(request, f'deleted email')
    return redirect(reverse('developmentEmailDashboard:inbox_view', args=(email,)))


def sendEmail(request, email):
    # sends a new email to email address
    toemails = []
    for em in json.loads(request.POST.get('to')):
        toemails.append(em['tag'])

    send_mail(
        request.POST.get('subject', ''),
        request.POST.get('content', ''),
        email,
        toemails,
        fail_silently=False,
    )
    messages.info(request, f'sent email to {toemails}')
    return redirect(reverse('developmentEmailDashboard:inbox_view', args=(email,)))


def deleteInbox(request, email):
    # deletes inbox with all of its emails
    inbox = get_object_or_404(Inbox, email=email)
    inbox.delete()
    messages.info(request, f'deleted Inbox "{email}"')
    return redirect(reverse('developmentEmailDashboard:inboxes_view'))


def createInboxView(request, email):
    # trys to create a new email and redirects to that
    # if the email inbox already exists redirects you to home page and sends message that the email already exists
    try:
        Inbox.objects.create(email=email)
        messages.success(request, f'created  {email} Inbox')
        return redirect(reverse('developmentEmailDashboard:inbox_view', args=(email,)))
    except:
        messages.error(request, f'cannot create Inbox with email "{email}" because it already exists')
        return redirect(reverse('developmentEmailDashboard:inboxes_view'))
