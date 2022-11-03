from django.db import models

class Voo(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    companhia_aerea = models.CharField(max_length=25)
    origem = models.CharField(max_length=25)
    destino = models.CharField(max_length=25)
    partida_prevista = models.TimeField()
    chegada_prevista = models.TimeField()

    class Meta:
        verbose_name = "Voo"
        verbose_name_plural = "Voos"

    def __str__(self):
        return self.codigo

class VooReal(models.Model):
    status_choices = (
        (0, ""),
        (-1, "Cancelado"),
        (1, "Embarcando"),
        (2, "Programado"),
        (3, "Taxiando"),
        (4, "Pronto"),
        (5, "Autorizado"),
        (6, "Em voo"),
        (7, "Aterrissado"),
    )

    status_dict = dict(status_choices)

    voo = models.ForeignKey(Voo, on_delete=models.CASCADE)
    dia = models.DateField()
    status = models.IntegerField(choices=status_choices, default=0)
    partida_real = models.TimeField(null=True, blank=True)
    chegada_real = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Voo Real"
        verbose_name_plural = "Voos Reais"
        constraints = [models.UniqueConstraint(fields=["voo", "dia"], name="unique_voo_dia")]

    def __str__(self):
        return self.voo.codigo + " - " + self.dia.strftime("%d/%m/%Y")
