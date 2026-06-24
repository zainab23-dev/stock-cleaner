from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'data', api_views.DataRowViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('edit/', api_views.edit_cell, name='api-edit-cell'),
    path('summary/', api_views.summary_metrics, name='api-summary'),
    path('upload/', api_views.upload_file_api, name='api-upload'),
    path('remove-oos/', api_views.remove_oos, name='api-remove-oos'),
    path('remove-fetch-error/', api_views.remove_fetch_error, name='api-remove-fetch-error'),
    path('delete/<int:item_id>/', api_views.delete_row, name='api-delete-row'),
    path('clear/', api_views.clear_all_data, name='api-clear'),
]
