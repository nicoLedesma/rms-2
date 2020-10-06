from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.admin.filters import RelatedFieldListFilter, FieldListFilter
from django.utils.encoding import smart_text
from django.db.models.fields import IntegerField, AutoField


class MultipleSelectFieldListFilter(FieldListFilter):

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s_filter' % field_path
        self.filter_statement = '%s__id' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        self.lookup_choices = field.get_choices(include_blank=False)
        super(MultipleSelectFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def values(self):
        """
        Returns a list of values to filter on.
        """
        values = []
        value = self.used_parameters.get(self.lookup_kwarg, None)
        if value:
            values = value.split(',')
        # convert to integers if IntegerField
        try:
            if type(self.field.rel.to._meta.pk) in [IntegerField, AutoField]:
                values = [int(x) for x in values]
        except:
            pass
        return values

    def queryset(self, request, queryset):
        raise NotImplementedError

    def choices(self, cl):
        yield {
            'selected': self.lookup_val is None,
            'query_string': cl.get_query_string({},
                [self.lookup_kwarg]),
            'display': _('All')
        }
        for pk_val, val in self.lookup_choices:
            selected = pk_val in self.values()
            pk_list = set(self.values())
            if selected:
                pk_list.remove(pk_val)
            else:
                pk_list.add(pk_val)
            queryset_value = ','.join([str(x) for x in pk_list])
            yield {
                'selected': selected,
                'query_string': cl.get_query_string({
                    self.lookup_kwarg: queryset_value,
                    }),
                'display': val,
            }


class IntersectionFieldListFilter(MultipleSelectFieldListFilter):
    """
    A FieldListFilter which allows multiple selection of
    filters for many-to-many type fields. A list of objects will be
    returned whose m2m contains all the selected filters.
    """

    def queryset(self, request, queryset):
        for value in self.values():
            filter_dct = {
                self.filter_statement: value
            }
            queryset = queryset.filter(**filter_dct)
        return queryset

#este es el que implementa
class UnionFieldListFilter(MultipleSelectFieldListFilter):
    """
    A FieldListFilter which allows multiple selection of
    filters for many-to-many type fields. A list of objects will be
    returned whose m2m contains all the selected filters.
    """

    def queryset(self, request, queryset):
        filter_statement = "%s__in" % self.filter_statement
        filter_values = self.values()
        filter_dct = {
            filter_statement: filter_values
        }
        if filter_values:
            print (filter_values)
            return queryset.filter(state__in = filter_values)
        else:
            return queryset
