from django.shortcuts import render
from .models import Voo, VooReal

# Create your views here.
def bookview(request):
    return render(request, "telaDeSelecao.html")


def areaDoOperador(request):
    if request.method == "POST":
        if request.POST.get("operation", "") == "create":
            Voo.objects.create(
                codigo=request.POST.get("codigo", ""),
                companhia_aerea=request.POST.get("companhia_aerea", ""),
                origem=request.POST.get("origem", ""),
                destino=request.POST.get("destino", ""),
                partida_prevista=request.POST.get("horario_partida_prevista", ""),
                chegada_prevista=request.POST.get("horario_chegada_prevista", ""),
            )
        elif request.POST.get("operation", "") == "delete":
            Voo.objects.get(codigo=request.POST.get("codigo", "")).delete()
        elif request.POST.get("operation", "") == "update":
            voo = Voo.objects.get(codigo=request.POST.get("codigo", ""))
            voo.companhia_aerea = request.POST.get("companhia_aerea", "")
            voo.origem = request.POST.get("origem", "")
            voo.destino = request.POST.get("destino", "")
            voo.partida_prevista = request.POST.get("horario_partida_prevista", "")
            voo.chegada_prevista = request.POST.get("horario_chegada_prevista", "")
            voo.save()

    context = {"voos": Voo.objects.all()}
    return render(request, "areaDoOperador.html", context)


def areaDoFuncionario(request):
    message = ""

    if request.method == "POST":
        vooReal = VooReal.objects.get(
            voo=Voo.objects.get(codigo=request.POST.get("codigo", ""))
        )
        
        if int(request.POST.get("status", "")) == vooReal.status + 1 or int(request.POST.get("status", "")) == -1:
            vooReal.status = request.POST.get("status", "")
            vooReal.save()
            message = "Status atualizado com sucesso!"
        else:
            message = "Status inválido"

    context = {"voosReais": VooReal.objects.all(), "status_dict": VooReal.status_dict, "message": message}
    return render(request, "areaDoFuncionario.html", context)


def areaDoGerente(request):
    return render(request, "areaDoGerente.html")


def cadastrarVoo(request):
    return render(request, "cadastrarVoo.html")


def consultarVoo(request):
    context = {"voo": Voo.objects.get(codigo=request.GET.get("codigo", ""))}
    return render(request, "consultarVoo.html", context)


def deletarVoo(request):
    return render(request, "deletarVoo.html")


def editarVoo(request):
    context = {"voo": Voo.objects.get(codigo=request.GET.get("codigo", ""))}
    context["voo"].partida_prevista = context["voo"].partida_prevista.strftime("%H:%M")
    context["voo"].chegada_prevista = context["voo"].chegada_prevista.strftime("%H:%M")

    return render(request, "editarVoo.html", context)


def relatorioVoos(request):
    return render(request, "relatorioVoos.html")
