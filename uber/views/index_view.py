from django.shortcuts import render, redirect
from uber.forms import CalculationForm
from django.urls import reverse


def index(request):  
    form_action = reverse('uber:index') 
    if request.method == 'POST':
        form = CalculationForm(request.POST)
        if form.is_valid():
            # Extraindo os dados do formulário
            data_criacao = form.cleaned_data['data_criacao']
            preco_comb = form.cleaned_data['preco_comb']
            desc_comb = form.cleaned_data['desc_comb']
            km_por_litro = form.cleaned_data['km_por_litro']
            km_rodado = form.cleaned_data['km_rodado']
            horas_trab = form.cleaned_data['horas_trab']
            faturamento = form.cleaned_data['faturamento']
            
            # convertento datas para string
            data_criacao = data_criacao.strftime('%Y-%m-%d')
            horas_trab = horas_trab.strftime('%H:%M')
            
            # transformando hora em decimal
            ganho_hora = (float(horas_trab[:2]) * 60 + float(horas_trab[3:5])) / 60
            
            # Realizando calculos
            comb_com_desc = round(preco_comb - desc_comb / 100 * preco_comb, 2)
            gasto_por_km = round(comb_com_desc / km_por_litro,2)
            gasto_com_comb = round(km_rodado * gasto_por_km,2)
            lucro = round(faturamento - gasto_com_comb,2)
            ganho_hora = round(lucro / ganho_hora,2)
            print(ganho_hora)
            ganho_por_km = round(lucro / km_rodado,2)
             
            # Criando a sessão 
            request.session['calculation_result'] = {
                'data_criacao': data_criacao,
                'gasto_por_km': gasto_por_km,
                'gasto_com_comb':gasto_com_comb,
                'comb_com_desc':comb_com_desc,
                'lucro':lucro,
                'ganho_por_km':ganho_por_km,
                'horas_trab':horas_trab,
                'km_rodado':km_rodado,
                'preco_comb':preco_comb,
                'faturamento':faturamento,
                'km_por_litro':km_por_litro,
                'ganho_hora':ganho_hora,
                'desc_comb':desc_comb,
                'owner':request.user.id,
            }
            
            # ResultUber.objects.create(
            #     gasto_por_km=gasto_por_km,
            #     gasto_com_comb=gasto_com_comb,
            #     comb_com_desc=comb_com_desc,
            #     lucro=lucro,
            #     ganho_por_km=ganho_por_km,
            # )
            return redirect('uber:result_view')
    else:         
        form = CalculationForm()
    return render(
        request,
        'uber/index.html',
        {
            'form': form,
            'form_action':form_action,
            'btn_text':'Calcular'
         }
    )
    