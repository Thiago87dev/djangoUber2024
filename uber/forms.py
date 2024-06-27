from django import forms

class CalculationForm(forms.Form):
    preco_comb = forms.FloatField(label='Preço do combustivel')
    desc_comb = forms.FloatField(label='Desconto do combustivel (em %)')
    km_por_litro = forms.FloatField(label='Quantos km seu carro faz por litro ?')
    km_rodado = forms.FloatField(label='Quantos km você rodou ?')
    faturamento = forms.FloatField(label='Quanto vecê faturou hoje ?')
    