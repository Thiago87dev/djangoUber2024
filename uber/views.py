from django.shortcuts import render, redirect, get_object_or_404
from .models import ResultUber
from .forms import CalculationForm

def index(request):
    if request.method == 'POST':
        form = CalculationForm(request.POST)
        if form.is_valid():
            preco_comb = form.cleaned_data['preco_comb']
            desc_comb = form.cleaned_data['desc_comb']
            km_por_litro = form.cleaned_data['km_por_litro']
            km_rodado = form.cleaned_data['km_rodado']
            faturamento = form.cleaned_data['faturamento']
            
            comb_com_desc = preco_comb - desc_comb / 100 * preco_comb
            gasto_por_km = comb_com_desc / km_por_litro
            gasto_com_comb = km_rodado * gasto_por_km
            lucro = faturamento - gasto_com_comb
            ganho_por_km = lucro / km_rodado
            
            request.session['calculation_result'] = {
                'gasto_por_km': gasto_por_km,
                'gasto_com_comb':gasto_com_comb,
                'comb_com_desc':comb_com_desc,
                'lucro':lucro,
                'ganho_por_km':ganho_por_km
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
            gasto_por_km=calculation_result['gasto_por_km'],
            gasto_com_comb=calculation_result['gasto_com_comb'],
            comb_com_desc=calculation_result['comb_com_desc'],
            lucro=calculation_result['lucro'],
            ganho_por_km=calculation_result['ganho_por_km'],
        )
        del request.session['calculation_result']
        return redirect('uber:result_detail',result_id=result.id)
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