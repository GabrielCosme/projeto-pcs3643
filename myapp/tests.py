from django.test import TestCase
from .models import Voo, VooReal


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
