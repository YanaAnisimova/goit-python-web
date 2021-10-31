from django.urls import path

from . import views


app_name = 'finance'

urlpatterns = [
    path('', views.index, name='index'),
    path('record', views.new_record_view, name='new_record'),
    path('reports', views.reports_view, name='reports'),
    # path('reports/detailed', views.income_reports, name='detailed'),
    # path('reports/categories', views.income_reports, name='categories'),
    # path('reports/months', views.income_reports, name='months'),
    ]
