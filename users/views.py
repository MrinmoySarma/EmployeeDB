from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
 
from .forms import UserRegistrationForm
from .tokens import account_activation_token




# Create your views here.

def login_user(request): 
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('User logged in successfully.'))
            return redirect('/')
        else:
            messages.success(request, ('Invalid Username or Password!'))
            return redirect('login')
    else:
        return render(request, 'users/login.html')
    

def logout_user(request):
    logout(request)
    messages.success(request, ('You were logged out!'))
    return redirect('/')



def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('users/template_activate_account.html', {
        'user': user.username, 
        'domain': get_current_site(request).domain, 
        'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
        'token': account_activation_token.make_token(user), 
        'protocol': 'https' if request.is_secure() else 'http',
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear {user.first_name}, please login to your Email- {to_email} for verification and completion of your registration. (NOTE: Also check spam folder)")
    else: 
        messages.error(request, f'Problem sending email to {to_email}, check if you have typed it correctly.')






def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, template_name='users/register_user.html', context={'form':form,})




def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login to your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('/')
