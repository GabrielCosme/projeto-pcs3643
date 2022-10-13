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