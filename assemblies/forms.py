import re

from django import forms

from .models import Assembly


class AssemblySearchForm(forms.Form):
    search_query = forms.CharField(
        label='Search by assembly designation or name',
        required=False,
    )


class AssemblyCreateAndUpdateForm(forms.ModelForm):

    designation = forms.CharField(
        label='Designation',
        help_text='Assembly designation can only contain numbers, '
                  'hyphens and dots.',
    )
    name = forms.CharField(
        label='Name',
        help_text='Assembly name can only contain letters, numbers and spaces.',
    )

    def clean_designation(self):
        msg_err = 'Invalid symbols! Assembly designation can only contain ' \
                  'numbers, hyphens and dots.'
        designation = self.cleaned_data['designation']
        if re.search(r'[^\d\-.]', designation):
            raise forms.ValidationError(msg_err)
        return designation

    def clean_name(self):
        msg_err = 'Invalid symbols! Assembly name can only contain letters, ' \
                  'numbers and spaces.'
        name = self.cleaned_data['name']
        if re.search(r'[^\d\sa-zA-Z]', name):
            raise forms.ValidationError(msg_err)
        return name

    class Meta:
        model = Assembly
        fields = '__all__'
