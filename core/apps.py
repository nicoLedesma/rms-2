# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from suit.apps import DjangoSuitConfig
from django.apps import AppConfig
#from suit.menu import ParentItem, ChildItem


class CoreConfig(AppConfig):
    name = 'Sistema de Reparaciones'
    verbose_name = "REGISTRO DE REPARACIONES DE EQUIPOS"
'''
class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
    verbose_name = 'Mi sitio comilon'
    admin_name = 'tomagay'
'''
#     menu = (
#         ParentItem('Clima', children=[
#             ChildItem(model='core.station'),
#             ChildItem(model='core.hardware'),
#             ChildItem(model='core.module'),
#             ChildItem(model='core.measure'),
#         ], icon='fa fa-leaf'),
#         ParentItem('Configuraciones de tipos', children=[
#             ChildItem(model='core.stationtype'),
#             ChildItem(model='core.moduletype'),
#             ChildItem(model='core.widget'),
#             ChildItem(model='core.hardwaretype'),
#         ], icon='fa fa-modx'),
#         ParentItem('Gestion de usuarios', children=[
#             ChildItem(model='users.user'),
#             ChildItem('Grupos', 'auth.group'),
#         ], icon='fa fa-users')
# )
