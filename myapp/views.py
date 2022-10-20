from django.shortcuts import render

# Create your views here.
def atualizarVooReal(request):
    return render(request, 'atualizarVooReal.html')

def cadastrarVoo(request):
    return render(request, 'cadastrarVoo.html')

def consultarVoo(request):
    return render(request, 'consultarVoo.html')

def deletarVoo(request):
    return render(request, 'deletarVoo.html')

def editarVoo(request):
    return render(request, 'editarVoo.html')

def relatorioVoos(request):
    return render(request, 'relatorioVoos.html')