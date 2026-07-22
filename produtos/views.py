from django.shortcuts import render # template + dados -> página
from django.contrib.auth.decorators import login_required #  um decorator (aquele @ que vai em cima da função). Ele "embrulha" a view e diz: "só deixa entrar quem está logado; se não estiver, manda pro LOGIN_URL". É assim que se protege uma página.

@login_required # O decorator
def home(request):
    return render(request, 'produtos/home.html')

