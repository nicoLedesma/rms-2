# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

STATES = (
    ('I','Ingresada'),
    ('D','Diagnósticando'),
    ('A','Esperando Aprobacion'),
    ('B','Aprobada'),
    ('N','No Aprobada'),
    ('W','Esperando Repuestos'),
    ('R','Reparando'),
    ('L','Lista'),
    ('E','Entregada'),
    ('S','No Se Pudo Reparar')
)

BRANCH = (
    ('BV', 'Los Boulevares'),
    ('PS', 'Punta del Sauce'),
    ('MN', 'Ministalalo')
)

MACHINE_TYPE = (
    ('W','Soldadora MMA'),
    ('P','Cortadora Plasma'),
    ('M','Soldadora MIG'),
    ('T','Soldadora TIG'),
    ('F','Soldadora TRIFASICA'),
    ('O','Otras Maquinas'),
)

GUARANTY = (
    ('G', 'Garantia'),
    ('B', 'Presupuestar')
    )


class Binnacle(models.Model):
    #description = models.CharField('Operación Realizada', null=True, max_length=255 )
    description = models.TextField('Operación Realizada:', null=True, blank=True)
    repair_sheet = models.ForeignKey('RepairSheet', on_delete=models.CASCADE,
                                     verbose_name="Hoja de Reparación")
    date = models.DateField('Fecha', auto_now_add=True)
    observation = models.TextField('Observaciones', null=True, blank=True)
    replacement_cost = models.TextField('Presupuesto Detallado', null=True, blank=True)

    def __str__(self):
        return "Bitacora del "'{}'.format(self.date)

    class Meta:
        verbose_name_plural = "Reparaciones"
        verbose_name = "Reparación"

class RepairSheet(models.Model):
    customer = models.CharField("Cliente", max_length=50, null=True, blank=True)
    branch = models.CharField("Sucursal", choices=BRANCH, max_length=25, default='BV')
    machine_type = models.CharField("Tipo", choices=MACHINE_TYPE, max_length=15, default='W')
    was_paid = models.BooleanField("Pagado", default=False)
    code = models.PositiveIntegerField("Codigo", default=1)
    in_date = models.DateField("Fecha de Ingreso")
    brand = models.CharField("Marca", max_length=25, null=True, blank=True)
    model = models.CharField("Modelo", max_length=25, null=True, blank=True )
    state = models.CharField("Estado", choices=STATES, max_length=15, default='I')
    out_date = models.DateField("Fecha de Entrega", null=True, blank=True)
    pre_diagnosis = models.CharField("Pre-Diagnóstico", max_length=100, default = "Sin datos suministrados")
    first_eye = models.TextField("Diagnóstico a primera vista", null=True, blank=True)
    fault_detected = models.TextField("Falla Detectada", null=True, blank=True)
    repair_cost = models.TextField("Costo de la Reparación", null=True, blank=True)
    type_of_repair = models.CharField("Tipo de Reparación", choices=GUARANTY, max_length=25, default='B')

    fault_image = models.ImageField("Cargar Imagen", null=True, blank=True, upload_to = 'images/repair_sheet')

    def __str__(self):
        return str(self.code_dalmaso)

    class Meta:
        verbose_name = "Hoja de Reparación"
        verbose_name_plural = "Hojas de Reparaciones"
