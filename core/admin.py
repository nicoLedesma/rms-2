# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.templatetags.static import static
from core.models import RepairSheet, Binnacle
from django import forms
from core.filter.filters import UnionFieldListFilter


class BinnacleForm(forms.ModelForm):
    class Media:
        js = (static('js/hide_add_binnacle.js'),)

    class Meta:
        model = Binnacle
        exclude = ()

class BinnacleForm_admin(forms.ModelForm):
    class Meta:
        model = Binnacle
        exclude = ()


class BinnacleInline(admin.TabularInline):
    model = Binnacle
    extra = 1
    #classes = ['collapse'] #para default admintheme
    #readonly_fields = ('date',)
    #classes = ['grp-collapse grp-closed'] #para grappelli

    fieldsets_Admin = ((None, {
            'fields': ('description', 'observation', 'replacement_cost')
        }),
        )

    fieldsets_Super = ((None, {
            'fields': ('description', 'replacement_cost')
        }),
        )


    fieldsets = ((None, {
            'fields': ('description',)
        }),
        )

    form = BinnacleForm

    #para ocultar elementos del form, no field del model
    def get_formset(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            print ("###soy superuser###")
            kwargs['form']= BinnacleForm_admin
            base_model_form = BinnacleForm_admin
        else:
            print ("###no soy superuser###")
        return super(BinnacleInline, self).get_formset(request, obj, **kwargs)

    #Para ocultar elementos del fieldset segun el model
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return self.fieldsets_Admin
        elif str(request.user)=="cristian":
            return self.fieldsets_Super
        else:
            return self.fieldsets


    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('date',)
            #return super(BinnacleInline, self).get_readonly_fields(request, obj)
        else:
            return ('date', 'description','replacement_cost')


class RepairSheetAdmin(admin.ModelAdmin):
    #change_list_template = "admin/change_list_filter_sidebar.html" #para cambiar la forma de visualizar el filtro en grappelli
    #change_list_filter_template = "admin/filter_listing.html" #para cambiar la forma de visualizar el filtro en grappelli

    #overide el metodo que muestra todas las repairsheets por defecto cuando cargo la pagina
    '''
    def changelist_view(self, request, extra_context=None):

        if not 'was_paid' in request.GET:
            q = request.GET.copy()
            q['was_paid'] = 'False'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(RepairSheetAdmin,self).changelist_view(request, extra_context=extra_context)
    '''
    def get_image(self, obj=None):
        if obj:
            return "<img width='250px' src='{}'>".format(obj.fault_image.url) #url es un atributo del image_field
        return ""

    get_image.allow_tags = True
    get_image.short_description = "Fotos"


    inlines = [
        BinnacleInline,
          ]

    fieldsets = (
        ('Datos', {
            'fields': ('code', ('branch', 'customer'), 'machine_type', 'brand', 'model','in_date', 'type_of_repair', 'state','out_date', 'was_paid')
        }),
        ('Diagnóstico', {
            #'classes': ('grp-collapse grp-closed',), #para grappelli
            #'classes': ('collapse',),
            'fields': ('pre_diagnosis','first_eye','fault_detected', 'repair_cost', 'get_image'),
        }),
    )

    fieldsets_Admin = (
        ('Datos', {
            'fields': ('code', ('branch', 'customer'), 'machine_type', 'brand', 'model','in_date', 'type_of_repair', 'state', 'out_date', 'was_paid')
        }),
        ('Diagnóstico', {
            #'classes': ('grp-collapse grp-closed',), #para grappelli
            #'classes': ('collapse',),
            'fields': ('pre_diagnosis','first_eye','fault_detected', 'repair_cost', 'get_image','fault_image'),
        }),
    )

    #Para ocultar elementos del fieldset segun el model
    def get_fieldsets(self, request, obj=None):
        print ("Este es el USUARIO: {}".format(request.user))
        if request.user.is_superuser:
            return self.fieldsets_Admin
        else:
            return self.fieldsets

    #Par el show
    #change_list_template = "custom_filter_state.html"

    list_display = ['code' , 'branch', 'brand', 'model', 'in_date', 'state', 'out_date', 'type_of_repair', 'was_paid']
    ordering = ['code']
    empty_value_display = '--'
    list_filter = (('state',UnionFieldListFilter),'was_paid','branch', 'brand', 'type_of_repair')
    search_fields = ('code', 'brand', 'model', 'fault_detected')
    readonly_fields = ('get_image',)


    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            #return ('repaired', 'first_eye')
            return super(RepairSheetAdmin, self).get_readonly_fields(request, obj)
        else:
            return ('code', 'branch', 'machine_type', 'customer', 'in_date', 'out_date', 'brand', 'model',
                    'state', 'pre_diagnosis', 'first_eye', 'fault_detected', 'repair_cost', 'type_of_repair',
                    'was_paid','get_image'
                    )


    def get_actions(self, request):
        actions = super(RepairSheetAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


    #Algunas pruebas
    #admin.site.disable_action('delete_selected')
    #exclude = ['code']
    #fields = ('code',('brans', 'model'), ('in_date','repaired','out_date')
    #          ,'pre_diagnosis','first_eye','fault_detected','repair_procedures')


# Register your models here.
#tiene que estar al final de las clases
admin.site.register(RepairSheet, RepairSheetAdmin)
#admin.site.register(Binnacle,)


'''
Some helps

# This ModelAdmin will not have delete_selected available
class SomeModelAdmin(admin.ModelAdmin):
    actions = ['some_other_action']
    ...

# This one will
class AnotherModelAdmin(admin.ModelAdmin):
    actions = ['delete_selected', 'a_third_action']
    ...
#Disabling all actions for a particular ModelAdmin
class MyModelAdmin(admin.ModelAdmin):
    actions = None


'''
