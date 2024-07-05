from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from uber.models import ResultUber
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
import datetime
from django.utils.safestring import mark_safe

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
            'faturamento'
        ]
    
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
           
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
    
    def clean_horas_trab(self):
        horas_trab = self.cleaned_data.get('horas_trab')
        
        if horas_trab == datetime.time(0,0):
            self.add_error(
                'horas_trab',
                ValidationError(
                    'Este campo não pode ser 0',
                    code='invalid'
                )
            )
        return horas_trab
    
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
    
    username = forms.CharField(
        required=True ,
        min_length=3,
        label='Usuário',
        help_text='Obrigatório. 150 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.'  
    )
    
    password1 = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput,
        help_text=mark_safe('Sua senha não pode ser muito semelhante às suas outras informações pessoais.<br>'
                   'Sua senha deve conter pelo menos 8 caracteres.<br>'
                   'Sua senha não pode ser uma senha comumente usada.<br>'
                   'Sua senha não pode ser totalmente numérica.')
    )
    
    password2 = forms.CharField(
        label='Confirmação de senha',
        strip=False,
        widget=forms.PasswordInput,
        help_text='Insira a mesma senha que foi digitada anteriormente, para verificação'
    )
    
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
                ValidationError('Um usuário com este email já existe.',code='invalid')
            )
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error(
                'username',
                ValidationError('Um usuário com este username já existe.',code='invalid')
            )
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        
        if password2 and len(password2) < 8:
            raise forms.ValidationError('Esta senha é muito curta. Deve conter pelo menos 8 caracteres.')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        
        return password2