from django.urls import path
from . import views

app_name = 'uber'

urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.filter, name='filter'),
    path('result/', views.result_view, name='result_view'),
    path('save/', views.save_result, name='save_result'),
    path('resultall/', views.result_all, name='result_all'),
    path('result/<int:result_id>/', views.result_detail, name='result_detail'),
    path('result/<int:result_id>/update/', views.update, name='update'),
    path('result/<int:result_id>/delete/', views.delete, name='delete'),
    path('monthly-summary/', views.monthly_summary, name='monthly_summary'),

    path('user/create/', views.createUser, name='create_user'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
]
