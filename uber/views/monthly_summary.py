from django.shortcuts import render
from uber.models import ResultUber
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Avg, Count
import math


def monthly_summary(request):
    start_year = 2014
    end_year = timezone.now().year

    summary_data = []

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):

            first_day = timezone.datetime(year, month, 1)
            if month == 12:
                last_day = timezone.datetime(
                    year + 1, 1, 1) - timedelta(days=1)
            else:
                last_day = timezone.datetime(
                    year, month + 1, 1) - timedelta(days=1)

            result = ResultUber.objects.filter(
                owner=request.user,
                data_criacao__gte=first_day,
                data_criacao__lte=last_day
            )

            if result:
                total_dias = result.aggregate(Count('id'))['id__count']
                total_faturamento = result.aggregate(Sum('faturamento'))[
                    'faturamento__sum']
                media_faturamento = round(result.aggregate(
                    Avg('faturamento'))['faturamento__avg'], 2)

                total_km_dirigido = round(result.aggregate(Sum('km_rodado'))[
                    'km_rodado__sum'], 2)
                media_km_dirigido = round(result.aggregate(
                    Avg('km_rodado'))['km_rodado__avg'], 2)

                total_gasto_comb = result.aggregate(Sum('gasto_com_comb'))[
                    'gasto_com_comb__sum']
                media_gasto_comb = round(result.aggregate(
                    Avg('gasto_com_comb'))['gasto_com_comb__avg'], 2)
                media_gasto_km = round(result.aggregate(
                    Avg('gasto_por_km'))['gasto_por_km__avg'], 2)
                media_lucro_km = round(result.aggregate(
                    Avg('ganho_por_km'))['ganho_por_km__avg'], 2)
                media_lucro_hora = round(result.aggregate(
                    Avg('ganho_hora'))['ganho_hora__avg'], 2)
                total_lucro = result.aggregate(Sum('lucro'))['lucro__sum']
                media_lucro = round(result.aggregate(
                    Avg('lucro'))['lucro__avg'], 2)

                # Pegando total de horas trabalhadas(em decimal)
                sql_horas_trab = ResultUber.objects.filter(
                    owner=request.user,
                    data_criacao__gte=first_day,
                    data_criacao__lte=last_day,
                ).values('horas_trab')
                total_horas_trab = 0
                for i in sql_horas_trab:
                    i['horas_trab'] = i['horas_trab'].strftime('%H-%M-%S')
                    total_horas_trab += (float(i['horas_trab'][:2])
                                         * 60 + float(i['horas_trab'][3:5])) / 60

                # Convertendo as horas(total) de decimal para horas
                total_horas = math.floor(total_horas_trab)
                total_minutos = math.floor(
                    (total_horas_trab - total_horas) * 60)
                # Formatando a hora(total)
                total_horas_trab_formatada = f'{total_horas}:{
                    str(total_minutos).zfill(2)}'

                # Pegando a media de horas trabalhada (em decimal)
                media_horas_trab = total_horas_trab / total_dias
                # Convertendo as horas(media) de decimal para horas
                media_horas = math.floor(media_horas_trab)
                media_minutos = math.floor(
                    (media_horas_trab - media_horas) * 60)
                # Formatando a hora(total)
                media_horas_trab_formatada = f'{media_horas}:{
                    str(media_minutos).zfill(2)}'

                summary_data.append({
                    'total_dias': total_dias,
                    'total_faturamento': total_faturamento,
                    'total_km_dirigido': total_km_dirigido,
                    'media_km_dirigido': media_km_dirigido,
                    'media_faturamento': media_faturamento,
                    'total_gasto_comb': total_gasto_comb,
                    'media_gasto_comb': media_gasto_comb,
                    'media_gasto_km': media_gasto_km,
                    'media_lucro_km': media_lucro_km,
                    'media_lucro_hora': media_lucro_hora,
                    'total_lucro': total_lucro,
                    'media_lucro': media_lucro,
                    'total_horas_trab': total_horas_trab_formatada,
                    'media_horas_trab': media_horas_trab_formatada,
                    'year': year,
                    'month': month,
                })

                context = {
                    'summary_data': summary_data,
                }
    return render(request, 'uber/monthly_summary.html', context)
