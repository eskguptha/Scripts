"""
django-admin-theme-custom-model-form
"""

from django.contrib import admin
from django import forms
from .models import MembershipRole
from django.contrib.admin.widgets import FilteredSelectMultiple

class MembershipRoleForm(forms.ModelForm):
    choices_list = MembershipRole.objects.all()
    groups = forms.ModelMultipleChoiceField(widget=FilteredSelectMultiple("Groups", is_stacked=False), queryset=choices_list)

    def __init__(self, *args, **kwargs):
        super(MembershipRoleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = MembershipRole
        fields = ()
        widgets = {

            'name': forms.TextInput(attrs={'class': 'selec2',
                                           'placeholder':
                                           'MembershipRolePermissions Name'}), 

            'allow_users': forms.Select(attrs={'class': 'form-control'}),
            }

class MembershipRoleAdmin(admin.ModelAdmin):
    form = MembershipRoleForm
    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/jsi18n',)

admin.site.register(MembershipRole, MembershipRoleAdmin)
