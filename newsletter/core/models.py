from django.db import models
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + str(self.confirmed) + ")"

class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='media/')

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def send(self):
        contents = self.contents.read().decode('utf-8')
        subscribers = Subscriber.objects.filter(confirmed=True)
        for sub in subscribers:
            message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject=self.subject,
                html_content=contents + '<br><a href="http://127.0.0.1:8000/delete/?email={}&conf_num={}">Unsubscribe</a>.'.format(sub.email, sub.conf_num))
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
