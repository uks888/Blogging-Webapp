import os
from django.core.mail import send_mail

# Set environment variables
def setVar():
    os.environ['EMAIL_USER'] = 'princepraa@gmail.com'
    os.environ['EMAIL_PASSWORD'] = 'Papamummy@05'

    send_mail(
        'Password Reset',
        'Reset your password from here',
        'princepraa@gmail.com',
        ['to@example.com'],
        fail_silently=False,
    )


