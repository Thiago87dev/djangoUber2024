from django.shortcuts import render, redirect, get_object_or_404
from uber.models import ResultUber
from uber.forms import CalculationForm
from django.contrib import messages

def delete(request, result_id):
    result = get_object_or_404(ResultUber, id=result_id)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Dados apagado com sucesso')
        return redirect('uber:result_all')
    
    