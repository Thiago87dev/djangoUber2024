from django.shortcuts import render, redirect, get_object_or_404
from .models import ResultUber
from .forms import CalculationForm
from django.utils import timezone
from datetime import timedelta

def index(request):
    
    if request.method == 'POST':
        form = CalculationForm(request.POST)
        if form.is_valid():
            data_criacao = form.cleaned_data['data_criacao']
            preco_comb = form.cleaned_data['preco_comb']
            desc_comb = form.cleaned_data['desc_comb']
            km_por_litro = form.cleaned_data['km_por_litro']
            km_rodado = form.cleaned_data['km_rodado']
            horas_trab = form.cleaned_data['horas_trab']
            faturamento = form.cleaned_data['faturamento']
            
            data_criacao = data_criacao.strftime('%Y-%m-%d')
            horas_trab = horas_trab.strftime('%H:%M')
            
            print(horas_trab, type(horas_trab))
            
            comb_com_desc = round(preco_comb - desc_comb / 100 * preco_comb, 2)
            gasto_por_km = round(comb_com_desc / km_por_litro,2)
            gasto_com_comb = round(km_rodado * gasto_por_km,2)
            lucro = round(faturamento - gasto_com_comb,2)
            ganho_por_km = round(lucro / km_rodado,2)
            # ganho_hora = horas_trab
            
        
            
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
                'horas_trab':horas_trab,
                # 'ganho_hora':ganho_hora
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
        {'form': form}
    )
    
def result_view(request):
    calculation_result = request.session.get('calculation_result')
    return render(
        request,
        'uber/result.html',
        {'result': calculation_result}
    )

def save_result(request):
    calculation_result = request.session.get('calculation_result')
    if calculation_result:
        result = ResultUber.objects.create(
            data_criacao=calculation_result['data_criacao'],
            gasto_por_km=calculation_result['gasto_por_km'],
            gasto_com_comb=calculation_result['gasto_com_comb'],
            comb_com_desc=calculation_result['comb_com_desc'],
            lucro=calculation_result['lucro'],
            ganho_por_km=calculation_result['ganho_por_km'],
            km_rodado=calculation_result['km_rodado'],
            preco_comb=calculation_result['preco_comb'],
            horas_trab=calculation_result['horas_trab'],
            # ganho_hora=calculation_result['ganho_hora']
            
        )
        del request.session['calculation_result']
        return redirect('uber:result_all')
    return redirect('uber:index')

def result_detail(request, result_id):
    result = get_object_or_404(ResultUber, id=result_id)
    return render(
        request,
        'uber/result_detail.html',
        {'result':result}
    )

def result_all(request):
   result = ResultUber.objects.all().order_by('-data_criacao') 
   return render(
       request,
       'uber/result_all.html',
       {'results':result }
   )