from django.test import TestCase
from .models import Voo, VooReal
from django.contrib.auth.models import User, Group, Permission


class test_view_login(TestCase):
    def test_login(self):
        self.client.logout()
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")


class test_view_auth(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="funcionario", password="bola1234")
        user.save()

    def test_voos(self):
        self.client.login(username="funcionario", password="bola1234")
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "telaDeSelecao.html")


class test_view_area_do_funcionario(TestCase):
    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(name="funcionario")
        group.permissions.add(
            Permission.objects.get(codename="add_vooreal"),
            Permission.objects.get(codename="change_vooreal"),
            Permission.objects.get(codename="delete_vooreal"),
            Permission.objects.get(codename="view_vooreal"),
            Permission.objects.get(codename="view_voo"),
        )
        user = User.objects.create_user(username="funcionario", password="bola1234")
        group.user_set.add(user)
        group.save()
        user.save()
        cls.voo = Voo.objects.create(
            codigo="AA123",
            companhia_aerea="ABC",
            origem="SP",
            destino="MG",
            partida_prevista="10:00",
            chegada_prevista="11:00",
        )
        cls.voo.save()

    def test_model_content(self):
        self.client.login(username="funcionario", password="bola1234")
        self.assertEqual(self.voo.codigo, "AA123")
        self.assertEqual(self.voo.companhia_aerea, "ABC")
        self.assertEqual(self.voo.origem, "SP")
        self.assertEqual(self.voo.destino, "MG")
        self.assertEqual(self.voo.partida_prevista, "10:00")
        self.assertEqual(self.voo.chegada_prevista, "11:00")

    def test_area_do_funcionario(self):
        self.client.login(username="funcionario", password="bola1234")
        response = self.client.get("/areaDoFuncionario/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "areaDoFuncionario.html")

    def test_funcionario_cria_voo_real(self):
        self.client.login(username="funcionario", password="bola1234")
        self.client.post(
            "/areaDoFuncionario/",
            {
                "operation": "create",
                "codigo": "AA123",
                "dia": "2020-01-01",
                "status": 0,
            },
            follow=True,
        )
        self.assertEqual(VooReal.objects.first().status, 0)

    def test_funcionario_altera_voo_real(self):
        self.client.login(username="funcionario", password="bola1234")
        VooReal.objects.create(voo=self.voo, dia="2020-01-01", status=0)
        self.client.post(
            "/areaDoFuncionario/",
            {
                "operation": "update",
                "codigo": "AA123",
                "dia": "2020-01-01",
                "status": 1,
            },
            follow=True,
        )
        self.assertEqual(VooReal.objects.first().status, 1)

    def test_funcionario_altera_ordem_invalida(self):
        self.client.login(username="funcionario", password="bola1234")
        VooReal.objects.create(voo=self.voo, dia="2020-01-01", status=0)
        self.client.post(
            "/areaDoFuncionario/",
            {
                "operation": "update",
                "codigo": "AA123",
                "dia": "2020-01-01",
                "status": 2,
            },
            follow=True,
        )
        self.assertEqual(VooReal.objects.first().status, 0)

    def test_cadastrar_voo_real(self):
        self.client.login(username="funcionario", password="bola1234")
        response = self.client.get("/cadastrarVooReal/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cadastrarVooReal.html")


class test_view_area_do_operador(TestCase):
    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(name="operador")
        group.permissions.add(
            Permission.objects.get(codename="add_voo"),
            Permission.objects.get(codename="change_voo"),
            Permission.objects.get(codename="delete_voo"),
            Permission.objects.get(codename="view_voo"),
            Permission.objects.get(codename="view_vooreal"),
        )
        user = User.objects.create_user(username="operador", password="bola1234")
        group.user_set.add(user)
        group.save()
        user.save()

        Voo.objects.create(
            codigo="ABC1342",
            companhia_aerea="GOL",
            origem="São Paulo",
            destino="Rio de Janeiro",
            partida_prevista="12:00",
            chegada_prevista="13:00",
        ).save()

    def test_area_do_operador(self):
        self.client.login(username="operador", password="bola1234")
        response = self.client.get("/areaDoOperador/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "areaDoOperador.html")

    def test_cadastrar_voo(self):
        self.client.login(username="operador", password="bola1234")
        response = self.client.get("/cadastrarVoo/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cadastrarVoo.html")

    def test_consultar_voo(self):
        self.client.login(username="operador", password="bola1234")
        response = self.client.get("/consultarVoo/?codigo=ABC1342", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "consultarVoo.html")

    def test_view_editar_voo(self):
        self.client.login(username="operador", password="bola1234")
        response = self.client.get("/editarVoo/?codigo=ABC1342", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "editarVoo.html")

    def test_cadastrar_voo(self):
        self.client.login(username="operador", password="bola1234")
        self.client.post(
            "/areaDoOperador/",
            {
                "operation": "create",
                "companhia_aerea": "LAT",
                "codigo": "123",
                "origem": "sp",
                "destino": "mg",
                "horario_partida_prevista": "00:10",
                "horario_chegada_prevista": "00:30",
            },
            follow=True,
        )
        self.assertEqual(Voo.objects.first().codigo, "123")

    def test_editar_voo(self):
        self.client.login(username="operador", password="bola1234")
        Voo.objects.create(
            codigo="123",
            companhia_aerea="123",
            origem="sp",
            destino="mg",
            partida_prevista="00:10",
            chegada_prevista="00:30",
        )
        self.client.post(
            "/areaDoOperador/",
            {
                "codigo": "123",
                "operation": "update",
                "companhia_aerea": "TAL",
                "origem": "sp",
                "destino": "mg",
                "horario_partida_prevista": "00:10",
                "horario_chegada_prevista": "00:30",
            },
            follow=True,
        )
        self.assertEqual(Voo.objects.first().companhia_aerea, "TAL")

    def test_deletar_voo(self):
        self.client.login(username="operador", password="bola1234")
        Voo.objects.create(
            codigo="123",
            companhia_aerea="123",
            origem="sp",
            destino="mg",
            partida_prevista="00:10",
            chegada_prevista="00:30",
        )
        itemCount = Voo.objects.count()
        self.client.post(
            "/areaDoOperador/", {"codigo": "123", "operation": "delete"}, follow=True
        )
        self.assertEqual(Voo.objects.count(), itemCount - 1)


class test_view_area_do_gerente(TestCase):
    @classmethod
    def setUpTestData(cls):
        group = Group.objects.create(name="gerente")
        group.permissions.add(
            Permission.objects.get(codename="view_voo"),
            Permission.objects.get(codename="view_vooreal"),
        )
        user = User.objects.create_user(username="gerente", password="bola1234")
        group.user_set.add(user)
        group.save()
        user.save()

    def test_area_do_gerente(self):
        self.client.login(username="gerente", password="bola1234")
        response = self.client.get("/areaDoGerente/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "areaDoGerente.html")

    def test_gera_relatorio_data(self):
        self.client.login(username="gerente", password="bola1234")
        response = self.client.post(
            "/areaDoGerente/",
            {
                "data_inicio": "2022-11-1",
                "data_fim": "2022-11-1",
                "companhia_aerea": "",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_gera_relatorio_cia_aerea(self):
        self.client.login(username="gerente", password="bola1234")
        response = self.client.post(
            "/areaDoGerente/",
            {"data_inicio": "", "data_fim": "", "companhia_aerea": "GOL"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_gera_relatorio_misto(self):
        self.client.login(username="gerente", password="bola1234")
        response = self.client.post(
            "/areaDoGerente/",
            {
                "data_inicio": "2022-11-1",
                "data_fim": "2022-11-1",
                "companhia_aerea": "GOL",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)


class VooTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Voo.objects.create(
            codigo="AA0001",
            companhia_aerea="American Airlines",
            origem="Miami",
            destino="São Paulo",
            partida_prevista="11:00",
            chegada_prevista="15:00",
        )

    def test_voo_codigo(self):
        voo = Voo.objects.get(codigo="AA0001")
        self.assertEqual(voo.codigo, "AA0001")

    def test_voo_companhia_aerea(self):
        voo = Voo.objects.get(codigo="AA0001")
        self.assertEqual(voo.companhia_aerea, "American Airlines")

    def test_voo_origem(self):
        voo = Voo.objects.get(codigo="AA0001")
        self.assertEqual(voo.origem, "Miami")

    def test_voo_destino(self):
        voo = Voo.objects.get(codigo="AA0001")
        self.assertEqual(voo.destino, "São Paulo")

    def test_voo_partida_prevista(self):
        voo = Voo.objects.get(codigo="AA0001")
        self.assertEqual(voo.partida_prevista.strftime("%H:%M"), "11:00")

    def test_voo_chegada_prevista(self):
        voo = Voo.objects.get(codigo="AA0001")
        self.assertEqual(voo.chegada_prevista.strftime("%H:%M"), "15:00")


class VooRealTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        voo = Voo.objects.create(
            codigo="AA0001",
            companhia_aerea="American Airlines",
            origem="Miami",
            destino="São Paulo",
            partida_prevista="11:00",
            chegada_prevista="15:00",
        )
        VooReal.objects.create(
            voo=voo,
            dia="2020-01-01",
            status=0,
            partida_real="11:00",
            chegada_real="15:00",
        )

    def test_voo_real_voo(self):
        voo_real = VooReal.objects.get(voo="AA0001")
        self.assertEqual(voo_real.voo.codigo, "AA0001")

    def test_voo_real_dia(self):
        voo_real = VooReal.objects.get(voo="AA0001")
        self.assertEqual(voo_real.dia.strftime("%Y-%m-%d"), "2020-01-01")

    def test_voo_real_status(self):
        voo_real = VooReal.objects.get(voo="AA0001")
        self.assertEqual(voo_real.status, 0)

    def test_voo_real_partida_real(self):
        voo_real = VooReal.objects.get(voo="AA0001")
        self.assertEqual(voo_real.partida_real.strftime("%H:%M"), "11:00")

    def test_voo_real_chegada_real(self):
        voo_real = VooReal.objects.get(voo="AA0001")
        self.assertEqual(voo_real.chegada_real.strftime("%H:%M"), "15:00")

    def test_voo_real_unique(self):
        voo = Voo.objects.get(codigo="AA0001")
        with self.assertRaises(Exception):
            VooReal.objects.create(
                voo=voo,
                dia="2020-01-01",
                status=1,
                partida_real="12:00",
                chegada_real="16:00",
            )
