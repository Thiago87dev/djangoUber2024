from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from uber.models import ResultUber
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Avg, Count
from django.core.paginator import Paginator
import math

@login_required(login_url='uber:login')
def filter(request):
    results = ResultUber.objects.filter(owner=request.user)
    
    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')
    order_by = request.GET.get('order_by', '-data_criacao')
    
    
    if start_date and end_date:
        
        # Convertendo string para data
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Fazendo a conulta com as datas
        results = results.filter(data_criacao__gte=start_date, data_criacao__lte=end_date)
    else:
        messages.error(request, 'Start date and end date are required.')
        return redirect('uber:result_all')
    
    # Lógica de ordenação
    if order_by.startswith('-'):
        order_by_field = order_by[1:]
        descending = True
    else:
        order_by_field = order_by
        descending = False
        
    results = results.order_by(('-' if descending else '') + order_by_field)
    
    paginator = Paginator(results, 31)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
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
        sql_horas_trab = ResultUber.objects.filter(owner=request.user,data_criacao__gte=start_date, data_criacao__lte=end_date)
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
        'results': page_obj,
        'order_by':order_by,
        'descending':descending,
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
        'mostrar_pagination': total_dias >= 31,
        }
            
        return render(
            request,
            'uber/result_all.html',
            context
        )
    else:
        
        context = {
            'results': results,
            'start_date':start_date.strftime('%Y-%m-%d'),
            'end_date':end_date.strftime('%Y-%m-%d'),
            'order_by': order_by_field,
            'descending': descending,
        }
        
        messages.info(request,'No data found'),
        return render(
            request,
            'uber/result_all.html',  
            context,
        )
    