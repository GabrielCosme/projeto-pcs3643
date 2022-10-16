from django.shortcuts import render

# Create your views here.


def bookview(request):
    return render(request, "telaDeSelecao.html")

def areaDoOperador(request):
    return render(request, "areaDoOperador.html")

def areaDoFuncionario(request):
    return render(request, "areaDoFuncionario.html")

def areaDoGerente(request):
    return render(request, "areaDoGerente.html")

def cadastrarVoo(request):
    return render(request, "cadastrarVoo.html")

def consultarVoo(request):
    return render(request, "consultarVoo.html")

def deletarVoo(request):    
    return render(request, "deletarVoo.html")

def editarVoo(request):
    return render(request, "editarVoo.html")

def relatorioVoos(request):
    return render(request, "relatorioVoos.html")

def atualizarVooReal(request):
    return render(request, "atualizarVooReal.html")

