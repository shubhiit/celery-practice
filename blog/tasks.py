from django.contrib.auth.models import User
from django.core.mail import send_mail
import time
from celery import shared_task

@shared_task
def send_email_interval(total):
    recievers = []
    subject = 'Task completed using celery'
    from_email = 'tiwarishubh24@gmail.com'
    for user in User.objects.all():
        recievers.append(user.email)
        count = 0
        while(count<total):
            message = 'This is ' + str(count) + 'time'
            send_mail(subject, message, from_email, recievers)
            time.sleep(3)
            count = count + 1
