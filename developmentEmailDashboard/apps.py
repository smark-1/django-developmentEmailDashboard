from django.apps import AppConfig


class DevelopmentemaildashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'developmentEmailDashboard'

    def ready(self):
        # setup signals for deleting a DevelopmentEmail when no InboxEmail objects are attached to it
        from . import signals
