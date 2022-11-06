from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Voo, VooReal
from datetime import datetime
import pytz


@login_required(login_url="/login/")
def bookview(request):
    return render(request, "telaDeSelecao.html")


@permission_required("myapp.change_voo", login_url="/login/")
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


@permission_required("myapp.change_vooreal", login_url="/login/")
def areaDoFuncionario(request):
    message = ""

    if request.method == "POST":
        if request.POST.get("operation", "") == "create":
            VooReal.objects.create(
                voo=Voo.objects.get(codigo=request.POST.get("codigo", "")),
                dia=request.POST.get("dia", ""),
            )
        elif request.POST.get("operation", "") == "update":
            vooReal = VooReal.objects.get(
                voo=Voo.objects.get(codigo=request.POST.get("codigo", "")),
                dia=request.POST.get("dia", ""),
            )

            if (
                int(request.POST.get("status", "")) == vooReal.status + 1
                or int(request.POST.get("status", "")) == -1
            ):
                vooReal.status = int(request.POST.get("status", ""))

                if vooReal.status == 7:
                    vooReal.partida_real = datetime.now(
                        pytz.timezone("America/Sao_Paulo")
                    ).time()
                elif vooReal.status == 8:
                    vooReal.chegada_real = datetime.now(
                        pytz.timezone("America/Sao_Paulo")
                    ).time()

                vooReal.save()
                message = "Status atualizado com sucesso!"
            else:
                message = "Status inválido"

    context = {
        "voosReais": VooReal.objects.all(),
        "status_dict": VooReal.status_dict,
        "message": message,
    }
    return render(request, "areaDoFuncionario.html", context)


@permission_required("myapp.add_vooreal", login_url="/login/")
def cadastrarVooReal(request):
    context = {"voos": Voo.objects.all()}
    return render(request, "cadastrarVooReal.html", context)


def areaDoGerente(request):
    context = {}

    if request.method == "POST":
        if request.POST.get("companhia_aerea", "") == "":
            context = {
                "voosReal": VooReal.objects.filter(
                    dia__gte=request.POST.get("data_inicio", ""),
                    dia__lte=request.POST.get("data_fim", ""),
                )
            }
        elif (
            request.POST.get("data_inicio", "") == ""
            and request.POST.get("data_fim", "") == ""
        ):
            context = {
                "voosReal": VooReal.objects.filter(
                    voo__companhia_aerea=request.POST.get("companhia_aerea", "")
                )
            }
        else:
            context = {
                "voosReal": VooReal.objects.filter(
                    dia__gte=request.POST.get("data_inicio", ""),
                    dia__lte=request.POST.get("data_fim", ""),
                    voo__companhia_aerea=request.POST.get("companhia_aerea", ""),
                )
            }

    return render(request, "areaDoGerente.html", context)


@permission_required("myapp.add_voo", login_url="/login/")
def cadastrarVoo(request):
    return render(request, "cadastrarVoo.html")


@permission_required("myapp.view_voo", login_url="/login/")
def consultarVoo(request):
    context = {"voo": Voo.objects.get(codigo=request.GET.get("codigo", ""))}
    return render(request, "consultarVoo.html", context)


@permission_required("myapp.delete_voo", login_url="/login/")
def deletarVoo(request):
    return render(request, "deletarVoo.html")


@permission_required("myapp.change_voo", login_url="/login/")
def editarVoo(request):
    context = {"voo": Voo.objects.get(codigo=request.GET.get("codigo", ""))}
    return render(request, "editarVoo.html", context)


def relatorioVoos(request):
    # context = {"voosReal": VooReal.objects.all()}
    return render(request, "relatorioVoos.html")
