from django.shortcuts import render, redirect, get_object_or_404
from uber.models import ResultUber
from django.db.models import Sum, Avg, Count
from django.contrib import messages
import math

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
        messages.success(request, 'Dados cadastrado com sucesso')
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
