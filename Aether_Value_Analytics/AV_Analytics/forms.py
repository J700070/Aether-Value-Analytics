from cProfile import label
from django.forms import ModelForm,TextInput
from .models import Company


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['ticker']
        # Used to apply CSS to the form
        widgets = {
            'ticker': TextInput(attrs={
                'class': 'appearance-none block w-1/2 bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white',
                'placeholder': 'Ticker',
                'required': 'required',
                }),
            

        }


