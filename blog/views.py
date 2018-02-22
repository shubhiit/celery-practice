from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.generic import View
from .forms import SignupForm, LoginForm
from django.core.mail import send_mail
from .tasks import send_email_interval
import time



def mail(request):
    recievers = []
    subject = 'Task completed and corrected'
    from_email = 'tiwarishubh24@gmail.com'
    for user in User.objects.all():
        recievers.append(user.email)
    total = 3
    count = 0
    while(count<total):
        message = 'Hello, I have done the assigned Task. This mail will be sent to you three times between interval of 10 minutes. This is the ' + str(count+1) + ' time. The current time is: ' + str(time.ctime())
        send_mail(subject, message, from_email, recievers)
        time.sleep(600)
        count = count + 1
    return HttpResponse("message sent")

def home(request):
    return render(request, 'blog/home.html')

def index(request):
    return HttpResponse('<h1>Login is successfull</h1>')

class LoginFormView(View):
    form_class = LoginForm
    template_name = 'blog/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            send_email_interval.delay(3)
            login(request, user)
            return redirect('blog:index')

        return render(request, 'blog/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('blog/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
               mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
        return render(request, 'blog/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')