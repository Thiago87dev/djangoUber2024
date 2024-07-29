from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from uber.models import ResultUber
from django.contrib import messages


@login_required(login_url='uber:login')
def delete(request, result_id):
    result = get_object_or_404(ResultUber, id=result_id, owner=request.user)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Data deleted successfully')
        return redirect('uber:result_all')
