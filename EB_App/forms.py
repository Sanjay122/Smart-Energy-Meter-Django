from django.forms import ModelForm
from . import models


class WithinADayDataModelForm(ModelForm):
    class Meta:
        model = models.WithinADayData
        fields = '__all__'
