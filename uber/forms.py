from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from uber.models import ResultUber
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
import datetime


class CalculationForm(forms.ModelForm):
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    now_in_sp = timezone.now().astimezone(sao_paulo_tz).strftime('%Y-%m-%d')

    class Meta:
        model = ResultUber
        fields = [
            'data_criacao',
            'preco_comb',
            'desc_comb',
            'km_por_litro',
            'km_rodado',
            'horas_trab',
            'faturamento',
            'observacao',
        ]

    data_criacao = forms.DateField(
        label='Date',
        required=True,
        initial=now_in_sp,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        ))
    preco_comb = forms.FloatField(
        label='Fuel price',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the fuel price'
            }
        ))
    desc_comb = forms.FloatField(
        label='Fuel discount (in %)',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the fuel discount',
            }
        ))
    km_por_litro = forms.FloatField(
        label='Vehicle autonomy',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter km per liter'
            }
        ))
    km_rodado = forms.FloatField(
        label='km driven',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter km driven'
            }
        ))
    horas_trab = forms.TimeField(
        label='Worked hours',
        required=False,
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'class': 'form-control',
                'placeholder': 'HH:MM',
                'type': 'time'
            }
        )
    )
    faturamento = forms.FloatField(
        label='Billings',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter billing'
            }
        ))

    observacao = forms.CharField(
        label='Note',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter note'
            }
        ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_km_por_litro(self):
        km_por_litro = self.cleaned_data.get('km_por_litro')

        if km_por_litro == 0:
            self.add_error(
                'km_por_litro',
                ValidationError(
                    'This field cannot be zero',
                    code='invalid'
                )
            )
        return km_por_litro

    def clean_km_rodado(self):
        km_rodado = self.cleaned_data.get('km_rodado')

        if km_rodado == 0:
            self.add_error(
                'km_rodado',
                ValidationError(
                    'This field cannot be zero',
                    code='invalid'
                )
            )
        return km_rodado

    def clean_horas_trab(self):
        horas_trab = self.cleaned_data.get('horas_trab')

        if horas_trab == datetime.time(0, 0):
            self.add_error(
                'horas_trab',
                ValidationError(
                    'This field cannot be zero',
                    code='invalid'
                )
            )
        return horas_trab


class CreationFormUser(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        required=True,
        min_length=3,
    )
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'A user with this email already exists.',
                        code='invalid')
                )
        return email
