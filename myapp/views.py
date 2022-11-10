from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Voo, VooReal
from datetime import datetime
import pytz


def check_status(vooReal, post_status):
    if vooReal.voo.tipo == "Partida":
        if (
            int(post_status) == vooReal.status + 1 or int(post_status) == -1
        ) and vooReal.status != 7:
            vooReal.status = int(post_status)

            if vooReal.status == 7:
                vooReal.horario_real = datetime.now(
                    pytz.timezone("America/Sao_Paulo")
                ).time()

            vooReal.save()
            return "Status atualizado com sucesso!"

        return "Status inválido"

    if vooReal.voo.tipo == "Chegada":
        if (
            int(post_status) == vooReal.status + 1
            or (
                vooReal.status == 0
                and (int(post_status) == 7 or int(post_status) == -1)
            )
        ) and vooReal.status != 8:
            vooReal.status = int(post_status)

            if vooReal.status == 8:
                vooReal.horario_real = datetime.now(
                    pytz.timezone("America/Sao_Paulo")
                ).time()

            vooReal.save()
            return "Status atualizado com sucesso!"

        return "Status inválido"


@login_required(login_url="/login/")
def bookview(request):
    return render(request, "telaDeSelecao.html")


@permission_required("myapp.change_voo", login_url="/login/")
def areaDoOperador(request):
    message = ""

    if request.method == "POST":
        if request.POST.get("operation", "") == "create":
            try:
                Voo.objects.create(
                    codigo=request.POST.get("codigo", ""),
                    companhia_aerea=request.POST.get("companhia_aerea", ""),
                    origem=request.POST.get("origem", ""),
                    destino=request.POST.get("destino", ""),
                    tipo=request.POST.get("tipo", ""),
                    horario_previsto=request.POST.get("horario_previsto", ""),
                )
            except:
                message = "Não foi possível criar o Voo: Código de Voo já existente"
        elif request.POST.get("operation", "") == "delete":
            Voo.objects.get(codigo=request.POST.get("codigo", "")).delete()
        elif request.POST.get("operation", "") == "update":
            voo = Voo.objects.get(codigo=request.POST.get("codigo", ""))
            voo.companhia_aerea = request.POST.get("companhia_aerea", "")
            voo.origem = request.POST.get("origem", "")
            voo.destino = request.POST.get("destino", "")
            voo.tipo = request.POST.get("tipo", "")
            voo.horario_previsto = request.POST.get("horario_previsto", "")
            voo.save()

    context = {"voos": Voo.objects.all(), "message": message}
    return render(request, "areaDoOperador.html", context)


@permission_required("myapp.change_vooreal", login_url="/login/")
def areaDoFuncionario(request):
    message = ""

    if request.method == "POST":
        if request.POST.get("operation", "") == "create":
            try:
                VooReal.objects.create(
                    voo=Voo.objects.get(codigo=request.POST.get("codigo", "")),
                    dia=request.POST.get("dia", ""),
                )
            except:
                message = "Não foi possível criar o VooReal: Combinação de Código de Voo e Dia já existente"
        elif request.POST.get("operation", "") == "update":
            vooReal = VooReal.objects.get(
                voo=Voo.objects.get(codigo=request.POST.get("codigo", "")),
                dia=request.POST.get("dia", ""),
            )

            message = check_status(vooReal, request.POST.get("status", ""))

    context = {
        "voosReais": VooReal.objects.all(),
        "partida_dict": dict(list(VooReal.status_dict.items())[:-1]),
        "chegada_dict": dict(
            list(VooReal.status_dict.items())[:2]
            + list(VooReal.status_dict.items())[-2:]
        ),
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
