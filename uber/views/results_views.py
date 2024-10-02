from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from uber.models import ResultUber
from django.db.models import Sum, Avg, Count
from django.core.paginator import Paginator
from django.contrib import messages
import math
from django.utils import timezone
from datetime import timedelta


def result_view(request):
    calculation_result = request.session.get('calculation_result')
    if calculation_result:
        return render(
            request,
            'uber/result.html',
            {'result': calculation_result}
        )
    return redirect('uber:index')


@login_required(login_url='uber:login')
def save_result(request):
    calculation_result = request.session.get('calculation_result')
    if calculation_result:

        user_id = calculation_result['owner']
        owner = get_object_or_404(User, id=user_id)

        ResultUber.objects.create(
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
            desc_comb=calculation_result['desc_comb'],
            observacao=calculation_result['observacao'],
            owner=owner
        )
        del request.session['calculation_result']
        messages.success(request, 'Data registered successfully')
        return redirect('uber:result_all')
    return redirect('uber:index')


@login_required(login_url='uber:login')
def result_detail(request, result_id):
    result = get_object_or_404(ResultUber, id=result_id)
    return render(
        request,
        'uber/result_detail.html',
        {'result': result}
    )


@login_required(login_url='uber:login')
def result_all(request):
    current_date = timezone.now()
    year_str = request.GET.get('year', current_date.year)
    month_str = request.GET.get('month', current_date.month)

    year = int(year_str)
    month = int(month_str)

    first_day = timezone.datetime(year, month, 1)
    if month == 12:
        last_day = timezone.datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = timezone.datetime(year, month + 1, 1) - timedelta(days=1)

    previous_month = (month - 1) if month > 1 else 12
    previous_year = year if month > 1 else year - 1
    next_month = (month + 1) if month < 12 else 1
    next_year = year if month < 12 else year + 1

    result = ResultUber.objects.filter(
        owner=request.user,
        data_criacao__gte=first_day,
        data_criacao__lte=last_day
    )

    if not result:
        if month > 1:
            first_day = timezone.datetime(year, month - 1, 1)
        else:
            first_day = timezone.datetime(year - 1, 12, 1)

        if month == 1:
            last_day = timezone.datetime(year, 1, 1) - timedelta(days=1)
        else:
            last_day = timezone.datetime(year, month, 1) - timedelta(days=1)

    result = ResultUber.objects.filter(
        owner=request.user,
        data_criacao__gte=first_day,
        data_criacao__lte=last_day
    )

    order_by = request.GET.get('order_by', '-data_criacao')
    if order_by.startswith('-'):
        descending = True
    else:
        descending = False

    result = result.order_by(order_by)

    paginator = Paginator([first_day], 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

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
        media_lucro = round(result.aggregate(Avg('lucro'))['lucro__avg'], 2)

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
        total_minutos = math.floor((total_horas_trab - total_horas) * 60)
        # Formatando a hora(total)
        total_horas_trab_formatada = f'{total_horas}:{
            str(total_minutos).zfill(2)}'

        # Pegando a media de horas trabalhada (em decimal)
        media_horas_trab = total_horas_trab / total_dias
        # Convertendo as horas(media) de decimal para horas
        media_horas = math.floor(media_horas_trab)
        media_minutos = math.floor((media_horas_trab - media_horas) * 60)
        # Formatando a hora(total)
        media_horas_trab_formatada = f'{media_horas}:{
            str(media_minutos).zfill(2)}'

        context = {
            'results': result,
            'page_obj': page_obj,
            'order_by': order_by,
            'descending': descending,
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
            'mostrar_pagination': total_dias >= 31,
            'year': year,
            'month': month,
            'current_date': current_date,
            'previous_year': previous_year,
            'previous_month': previous_month,
            'next_year': next_year,
            'next_month': next_month,
        }
    else:
        context = {
            'empty': 'Nothing here',
        }
    return render(
        request,
        'uber/result_all.html',
        context
    )
