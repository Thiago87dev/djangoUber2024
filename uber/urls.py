from django.urls import path
from . import views

app_name = 'uber'

urlpatterns = [
    path('',views.index, name='index'),
    path('result/',views.result_view, name='result_view'),
    path('save/',views.save_result, name='save_result'),
    path('resultall/',views.result_all, name='result_all'),
    path('result/<int:result_id>',views.result_detail, name='result_detail'),
]