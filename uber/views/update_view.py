from django.shortcuts import render, redirect, get_object_or_404
from uber.models import ResultUber
from uber.forms import CalculationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='uber:login')
def update(request, result_id):
    result = get_object_or_404(ResultUber, id=result_id, owner=request.user)

    if request.method == 'POST':
        form = CalculationForm(request.POST, instance=result)
        if form.is_valid():

            # Extraindo os dados do formulário
            data_criacao = form.cleaned_data['data_criacao']
            preco_comb = form.cleaned_data['preco_comb']
            desc_comb = form.cleaned_data['desc_comb']
            km_por_litro = form.cleaned_data['km_por_litro']
            km_rodado = form.cleaned_data['km_rodado']
            horas_trab = form.cleaned_data['horas_trab']
            faturamento = form.cleaned_data['faturamento']

            # Convertendo datas para string
            horas_trab_str = horas_trab.strftime('%H:%M')

            # Transformando hora em decimal
            ganho_hora = (
                float(horas_trab_str[:2]) * 60 +
                float(horas_trab_str[3:5])) / 60

            # Realizando calculos
            comb_com_desc = round(preco_comb - desc_comb / 100 * preco_comb, 2)
            gasto_por_km = round(comb_com_desc / km_por_litro, 2)
            gasto_com_comb = round(km_rodado * gasto_por_km, 2)
            lucro = round(faturamento - gasto_com_comb, 2)
            ganho_hora = round(lucro / ganho_hora, 2)
            ganho_por_km = round(lucro / km_rodado, 2)

            # Atualizando os campos do objeto result
            result.data_criacao = data_criacao
            result.preco_comb = preco_comb
            result.desc_comb = desc_comb
            result.km_por_litro = km_por_litro
            result.km_rodado = km_rodado
            result.horas_trab = horas_trab
            result.faturamento = faturamento
            result.comb_com_desc = comb_com_desc
            result.gasto_por_km = gasto_por_km
            result.gasto_com_comb = gasto_com_comb
            result.lucro = lucro
            result.ganho_hora = ganho_hora
            result.ganho_por_km = ganho_por_km

            result.save()
            messages.success(request, 'Data updated successfully')
            return redirect('uber:result_all')
    else:
        form = CalculationForm(instance=result)

    return render(
        request,
        'uber/index.html',
        {
            'form': form,
            'result': result,
            'btn_text': 'Update'
        }
    )
