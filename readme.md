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
    * optional to get windows notifications install zroya `pip install zroya`
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

## configuration
#### get notified when you receive an email
in settings.py set`DEVELOPMENT_EMAIL_DASHBOARD_SEND_EMAIL_NOTIFICATION = True` to get a windows notification 
every time an email is received
> must have zroya installed | `pip install zroya`

## changelog
### 2.0.0 
added windows notifications

fixed bug where text based emails don't display new lines properly

fixed bug where deleting inbox creates does not exist error

## still left to do
* amazing documentation
* 100% testing coverage
* fix icons displaying centered
* render emails as they will be displayed in a email application not just html 
* option to show raw email with headers
* add email attachments
* allow browser to send html emails not just view emails with html sent by websites
* management command to delete database tables, clear tables, create tables again

> Any contribution is welcome just make a pull request, and I will try to add your feature in the next version as soon as possible.