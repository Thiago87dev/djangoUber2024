from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

class CalculationForm(forms.Form):
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    now_in_sp = timezone.now().astimezone(sao_paulo_tz).strftime('%Y-%m-%d')
    data_criacao = forms.DateField(
        label='Data',
        required=True,
        initial=now_in_sp,
        widget=forms.DateInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
    ))
    preco_comb = forms.FloatField(
        label='Preço do combustivel',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'placeholder':'Digite o preço do combustivel'
            }
    ))
    desc_comb = forms.FloatField(
        label='Desconto do combustivel (em %)',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'placeholder':'Digite o desconto do combustivel',
            }
    ))
    km_por_litro = forms.FloatField(
        label='Quantos km seu carro faz por litro ?',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'placeholder':'Digite km por litro'
            }
    ))
    km_rodado = forms.FloatField(
        label='Quantos km você rodou ?',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'placeholder':'Digite km rodado'
            }
    ))
    horas_trab = forms.TimeField(
        label='Horas trabalhada',
        required=False,
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'class':'form-control',
                'placeholder':'HH:MM',
                'type':'time'
            }
        )
    )
    faturamento = forms.FloatField(
        label='Faturamento',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'placeholder':'Digite o faturamento'
            }
    ))
    
    
    def clean_km_por_litro(self):
        km_por_litro = self.cleaned_data.get('km_por_litro')
        
        if km_por_litro == 0:
            self.add_error(
                'km_por_litro',
                ValidationError(
                    'Este campo não pode ser 0',
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
                    'Este campo não pode ser 0',
                    code='invalid'
                )
            )
        return km_rodado
    
class CreationFormUser(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
        label='Primeiro nome',
    )
    last_name = forms.CharField(
        required=True,
        min_length=3,
        label='Sobrenome ',
        )
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2',
        )
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Um usuário ocom este email já existe.')
            )
        return email

   