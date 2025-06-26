from django import forms
from django.forms import inlineformset_factory
from .models import Pferd, Fuetterung


# Pferd-Hauptformular
class PferdForm(forms.ModelForm):
    class Meta:
        model = Pferd
        fields = ['name', 'transponder_id', 'paddock_nummer', 'bild']

# Eigene Zeitfeld-Darstellung (HTML5 'time' Input)
class CustomTimeWidget(forms.TimeInput):
    input_type = 'time'
    format = '%H:%M'

# Formular für ein einzelnes Fütterungsintervall
class FuetterungForm(forms.ModelForm):
    class Meta:
        model = Fuetterung
        fields = ['start_zeit', 'end_zeit']
        widgets = {
            'start_zeit': CustomTimeWidget(attrs={'class': 'form-control'}),
            'end_zeit': CustomTimeWidget(attrs={'class': 'form-control'}),
        }

# Formularsatz für mehrere Zeitintervalle, verknüpft mit einem Pferd
FuetterungFormSet = inlineformset_factory(
    Pferd,
    Fuetterung,
    form=FuetterungForm,
    extra=1,
    can_delete=True
)

class ZugangForm(forms.Form):
    transponder_id = forms.CharField(
        label='Pferd-ID (Transponder)',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


