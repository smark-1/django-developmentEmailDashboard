# django-developmentEmailDashboard

A django email backend that saves the emails to database instead of sending them
and can view the emails in a web-browser

> :warning: disclaimer: do not use this in production or on any public server.
> this app hardly has any security protocols inplace since 
> this is meant to be used in development and values ease of use over security. 
> for example there is no password required to view a users inbox or to create a new one
> or for anything else. 



## Installation
1. prerequisites
    * must have static files configured
2. run `pip install django-developmentEmailDashboard`
3. Add 'developmentEmailDashboard' to your INSTALLED_APPS setting.
4. Add urls (only add the urls file that you plan on using)

      
      from django.conf import settings
      # ...
      if settings.DEBUG:
         urlpatterns.append(path('emails/', include('developmentEmailDashboard.urls')))

5. set the email backend in settings.py


    if DEBUG:
        EMAIL_BACKEND = 'developmentEmailDashboard.emailbackend.developmentEmailBackend'

6. Run the command `manage.py migrate`.


now every time you send an email it will show up on your website at  http://localhost:8000/emails/

> there is no validation on the emails that get created in the dashboard.
> for example you can create a inbox `test` or `@@@` and it will work this is done for convenience
> if users want this functionality to be changed that can be done

## still left to do
* amazing documentation
* 100% testing coverage
* notify user when a new email is received
* fix icons
* render emails as they will be displayed in a email application not just html 
* option to show raw email with headers
* add email attachments
* allow browser to send html emails not just view emails with html sent by websites

> Any contribution is welcome just make a pull request, and I will try to add your feature in the next version as soon as possible.