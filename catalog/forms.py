from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django import forms
from django.forms import BooleanField
from django.forms import ModelForm
from catalog.models import Product, Version
from django.core.exceptions import ValidationError


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field, in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):

    forbidden_words = [
        'казино',
        'криптовалюта',
        'крипта',
        'биржа',
        'дешево',
        'бесплатно',
        'обман',
        'полиция',
        'радар']

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {'created_at': forms.DateInput(attrs={'type': 'date', 'format':'yyyy-mm-dd'}),
                   'updated_at': forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'})}

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        for word in self.forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('В названии не должно быть запрещенных слов')
        return cleaned_data


    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for word in self.forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('В названии не должно быть запрещенных слов')
        return cleaned_data


class ModeratorProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'status',)
        widgets = {
            'status': forms.CheckboxInput(),
        }


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = "__all__"