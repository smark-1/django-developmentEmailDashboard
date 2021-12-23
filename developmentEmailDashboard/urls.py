from django.urls import path
from . import views

app_name = 'developmentEmailDashboard'

urlpatterns = [
    path('', views.inboxesView, name='inboxes_view'),
    path('create/<str:email>/', views.createInboxView, name='create_inbox_view'),
    path('<str:email>/', views.inboxView, name='inbox_view'),
    path('<str:email>/<int:id>/', views.emailView, name='email_view'),
    path('<str:email>/<int:id>/delete/', views.deleteEmail, name='delete_email'),
    path('<str:email>/<int:id>/sendemail/', views.replyEmail, name='reply_view'),
    path('<str:email>/sendemail/', views.sendEmail, name='send_email_view'),
    path('<str:email>/delete/', views.deleteInbox, name='delete_inbox_view'),
]