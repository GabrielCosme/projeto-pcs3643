from django.shortcuts import render
from .models import Voo, VooReal

# Create your views here.
def bookview(request):
    return render(request, "telaDeSelecao.html")


def areaDoOperador(request):
    if request.GET.get("codigo", "") != "":
        Voo.objects.get(codigo=request.GET.get("codigo", "")).delete()

    context = {"voos": Voo.objects.all()}
    return render(request, "areaDoOperador.html", context)


def areaDoFuncionario(request):
    if request.method == "POST":
        vooReal = VooReal.objects.get(
            voo=Voo.objects.get(codigo=request.POST.get("codigo", ""))
        )
        vooReal.status = request.POST.get("status", "")
        vooReal.save()

    context = {"voosReais": VooReal.objects.all(), "status_dict": VooReal.status_dict}
    return render(request, "areaDoFuncionario.html", context)


def areaDoGerente(request):
    return render(request, "areaDoGerente.html")


def cadastrarVoo(request):
    message = ""

    if request.method == "POST":
        Voo.objects.create(
            codigo=request.POST.get("codigo", ""),
            companhia_aerea=request.POST.get("companhia_aerea", ""),
            origem=request.POST.get("origem", ""),
            destino=request.POST.get("destino", ""),
            partida_prevista=request.POST.get("horario_partida_prevista", ""),
            chegada_prevista=request.POST.get("horario_chegada_prevista", ""),
        )

        message = "Voo cadastrado com sucesso"

    context = {"message": message}
    return render(request, "cadastrarVoo.html", context)


def consultarVoo(request):
    context = {"voo": Voo.objects.get(codigo=request.GET.get("codigo", ""))}
    return render(request, "consultarVoo.html", context)


def deletarVoo(request):
    return render(request, "deletarVoo.html")


def editarVoo(request):
    if request.method == "POST":
        voo = Voo.objects.get(codigo=request.POST.get("codigo", ""))
        voo.companhia_aerea = request.POST.get("companhia_aerea", "")
        voo.origem = request.POST.get("origem", "")
        voo.destino = request.POST.get("destino", "")
        voo.partida_prevista = request.POST.get("horario_partida_prevista", "")
        voo.chegada_prevista = request.POST.get("horario_chegada_prevista", "")
        voo.save()

        context = {"voo": Voo.objects.get(codigo=request.POST.get("codigo", ""))}
        message = "Voo editado com sucesso"
        context.update({"message": message})
    else:
        context = {"voo": Voo.objects.get(codigo=request.GET.get("codigo", ""))}

    return render(request, "editarVoo.html", context)


def relatorioVoos(request):
    return render(request, "relatorioVoos.html")
