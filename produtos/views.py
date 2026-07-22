from django.shortcuts import render, redirect, get_object_or_404 # template + dados -> página
from django.contrib.auth.decorators import login_required #  um decorator (aquele @ que vai em cima da função). Ele "embrulha" a view e diz: "só deixa entrar quem está logado; se não estiver, manda pro LOGIN_URL". É assim que se protege uma página.
from .models import Produto # Importa o modelo Produto
from .forms import ProdutoForm # Importa a classe ProdutoForm que foi criada

@login_required # O decorator
def home(request):
    return render(request, 'produtos/home.html')

@login_required
def produto_list(request):
    q = request.GET.get('q', '')
    produtos = Produto.objects.all()
    if q:
        produtos = produtos.filter(nome__icontains=q)
    produtos = produtos.order_by('-criado_em')
    return render(request, 'produtos/produto_list.html', {'produtos': produtos, 'q': q})

@login_required
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produto_list')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/produto_form.html', {'form': form})

@login_required
def produto_update(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produto_list')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/produto_form.html', {'form': form})

@login_required
def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('produto_list')
    return render(request, 'produtos/produto_confirm_delete.html', {'produto': produto})

