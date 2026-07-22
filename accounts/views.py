from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
           user = form.save(commit=False) # Cria o objeto na memória, mas não grava ainda
           user.is_active = False # Nasce "congelado": não pode logar
           user.save() # Agora sim grava no banco

           uid = urlsafe_base64_encode(force_bytes(user.pk))
           token = default_token_generator.make_token(user)
           activation_path = reverse('activate', kwargs={'uid64': uid, 'token': token})
           activation_url = request.build_absolute_uri(activation_path)
           
           send_mail(
            subject='Ative sua Conta',
            message=f'Ola {user.username}, clique para ativar sua conta:\n\n{activation_url}',
            from_email='no-reply@qastudy.local',
            recipient_list=[user.email],
           )
           return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uid64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:  
        return render(request, 'registration/activation_invalid.html')

