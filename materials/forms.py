import re

from django import forms
from materials.models import Material


class MaterialSearchForm(forms.Form):
    name = forms.CharField(
        label='Search by material name',
        required=False,
    )


class MaterialCreateAndUpdateForm(forms.ModelForm):
    name = forms.CharField(
        label='Material name',
        help_text='Material name can only contain letters, numbers and spaces.',
    )
    density = forms.IntegerField(
        label='Material density',
        help_text='Material density value must be positive integer.',
        required=False,
        min_value=0,
    )

    def clean_name(self):
        msg_err = 'Invalid symbols! Material name can only contain letters, ' \
                  'numbers and spaces.'
        name = self.cleaned_data['name']
        if re.search(r'[^\d\sa-zA-Z]', name):
            raise forms.ValidationError(msg_err)
        return name

    class Meta:
        model = Material
        fields = ('name', 'density',)
