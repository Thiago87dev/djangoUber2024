from django.shortcuts import render, redirect
from uber.models import ResultUber
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Avg, Count
import math

def filter(request):
    results = ResultUber.objects.all()
    
    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')
    if not start_date or not end_date:
        return redirect('uber:result_all')
    # Convertendo string para data
    start_date = timezone.datetime.strptime(start_date,'%Y-%m-%d').date() 
    end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
    
    results = results.filter(data_criacao__gte=start_date, data_criacao__lte=end_date).order_by('-data_criacao')
    
    if results.exists():
        total_dias = results.aggregate(Count('id'))['id__count']
        total_faturamento = results.aggregate(Sum('faturamento'))['faturamento__sum']
        media_faturamento = round(results.aggregate(Avg('faturamento'))['faturamento__avg'],2)
        total_gasto_comb = results.aggregate(Sum('gasto_com_comb'))['gasto_com_comb__sum']
        media_gasto_comb = round(results.aggregate(Avg('gasto_com_comb'))['gasto_com_comb__avg'],2)
        media_gasto_km = round(results.aggregate(Avg('gasto_por_km'))['gasto_por_km__avg'],2)
        media_lucro_km = round(results.aggregate(Avg('ganho_por_km'))['ganho_por_km__avg'],2)
        media_lucro_hora = round(results.aggregate(Avg('ganho_hora'))['ganho_hora__avg'],2)
        total_lucro = results.aggregate(Sum('lucro'))['lucro__sum']
        media_lucro = round(results.aggregate(Avg('lucro'))['lucro__avg'],2)
    
        # Pegando total de horas trabalhadas(em decimal)
        sql_horas_trab = ResultUber.objects.filter(data_criacao__gte=start_date, data_criacao__lte=end_date)
        total_horas_trab = 0
        for i in sql_horas_trab:
        
            horas_trab = i.horas_trab
            i.horas_trab = i.horas_trab.strftime('%H-%M-%S')
            total_horas_trab += (float(i.horas_trab[:2]) * 60 + float(i.horas_trab[3:5])) / 60
    
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
        'results': results,
        'start_date':start_date.strftime('%Y-%m-%d'),
        'end_date':end_date.strftime('%Y-%m-%d'),
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
    else:
        
        messages.info(request,'Nenhum dado encontrado'),
        return render(
            request,
            'uber/result_all.html',  
        )
    