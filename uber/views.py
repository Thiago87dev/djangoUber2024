from django.shortcuts import render, redirect, get_object_or_404
from .models import ResultUber
from .forms import CalculationForm
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Avg, Count
import math

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
            
            # convertento datas para string
            data_criacao = data_criacao.strftime('%Y-%m-%d')
            horas_trab = horas_trab.strftime('%H:%M')
            
            # transformando hora em decimal
            ganho_hora = (float(horas_trab[:2]) * 60 + float(horas_trab[3:5])) / 60
            
            comb_com_desc = round(preco_comb - desc_comb / 100 * preco_comb, 2)
            gasto_por_km = round(comb_com_desc / km_por_litro,2)
            gasto_com_comb = round(km_rodado * gasto_por_km,2)
            lucro = round(faturamento - gasto_com_comb,2)
            ganho_hora = round(lucro / ganho_hora,2)
            print(ganho_hora)
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
                'faturamento':faturamento,
                'km_por_litro':km_por_litro,
                'ganho_hora':ganho_hora,
                'desc_comb':desc_comb,
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
            faturamento=calculation_result['faturamento'],
            km_por_litro=calculation_result['km_por_litro'],
            ganho_hora=calculation_result['ganho_hora'],
            desc_comb=calculation_result['desc_comb']
            
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
   total_dias = result.aggregate(Count('id'))['id__count']
   total_faturamento = result.aggregate(Sum('faturamento'))['faturamento__sum']
   media_faturamento = round(result.aggregate(Avg('faturamento'))['faturamento__avg'],2)
   total_gasto_comb = result.aggregate(Sum('gasto_com_comb'))['gasto_com_comb__sum']
   media_gasto_comb = round(result.aggregate(Avg('gasto_com_comb'))['gasto_com_comb__avg'],2)
   media_gasto_km = round(result.aggregate(Avg('gasto_por_km'))['gasto_por_km__avg'],2)
   media_lucro_km = round(result.aggregate(Avg('ganho_por_km'))['ganho_por_km__avg'],2)
   media_lucro_hora = round(result.aggregate(Avg('ganho_hora'))['ganho_hora__avg'],2)
   total_lucro = result.aggregate(Sum('lucro'))['lucro__sum']
   media_lucro = round(result.aggregate(Avg('lucro'))['lucro__avg'],2)
   
   # Pegando total de horas trabalhadas(em decimal)
   sql_horas_trab = ResultUber.objects.values('horas_trab')
   total_horas_trab = 0
   for i in sql_horas_trab:
       horas_trab = i['horas_trab']
       i['horas_trab'] = i['horas_trab'].strftime('%H-%M-%S')
       total_horas_trab += (float(i['horas_trab'][:2]) * 60 + float(i['horas_trab'][3:5])) / 60
   
   # Convertendo as horas(total) de decimal para horas  
   total_horas = math.floor(total_horas_trab)
   total_minutos = math.floor((total_horas_trab - total_horas) * 60)
   # Formatando a hora(total)
   total_horas_trab_formatada = f'{total_horas}:{total_minutos}'

   # Pegando a media de horas trabalhada (em decimal)
   media_horas_trab = total_horas_trab / total_dias
   # Convertendo as horas(media) de decimal para horas 
   media_horas = math.floor(media_horas_trab)
   media_minutos = math.floor((media_horas_trab - media_horas) * 60)
   # Formatando a hora(total)
   media_horas_trab_formatada = f'{media_horas}:{media_minutos}'
   
   
   
   context = {
       'results':result,
       'total_dias':total_dias,
       'total_faturamento':total_faturamento,
       'media_faturamento':media_faturamento,
       'total_gasto_comb':total_gasto_comb,
       'media_gasto_comb':media_gasto_comb,
       'media_gasto_km':media_gasto_km,
       'media_lucro_km':media_lucro_km,
       'media_lucro_hora':media_lucro_hora,
       'total_lucro':total_lucro,
       'media_lucro':media_lucro,
       'total_horas_trab':total_horas_trab_formatada,
       'media_horas_trab':media_horas_trab_formatada,
    }
   return render(
       request,
       'uber/result_all.html',
       context
   )