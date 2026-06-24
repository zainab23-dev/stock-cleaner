from django.urls import path
from . import views, reports

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_file, name='upload'),
    path('reports/csv/', reports.csv_report, name='csv-report'),
    path('reports/excel/', reports.excel_report, name='excel-report'),
    path('reports/pdf/', reports.pdf_report, name='pdf-report'),
]
