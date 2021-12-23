from django.test import TestCase

# I don't know how to test sending emails because django switches the email backend to
# django.core.mail.backends.locmem.EmailBackend for testing
# if someone would like to contribute tests that run only in development that would be greatly appreciated
