from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import DataRow
from .serializers import DataRowSerializer
from .utils import sanitize_input
from .middleware import AuditLogMiddleware
from apps.trash.models import Trash

class DataRowViewSet(viewsets.ModelViewSet):
    queryset = DataRow.objects.all()
    serializer_class = DataRowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None          # <-- RETURN ALL ROWS

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return DataRow.objects.filter(status=status)
        return DataRow.objects.all()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_cell(request):
    row_id = request.data.get('id')
    field = request.data.get('field')
    value = request.data.get('value')
    if not all([row_id, field]):
        return Response({'error': 'Missing fields'}, status=400)
    if request.user.role not in ['Admin', 'Editor']:
        return Response({'error': 'Permission denied'}, status=403)
    row = get_object_or_404(DataRow, id=row_id)
    value = sanitize_input(value) if value is not None else value
    new_data = dict(row.data)
    new_data[field] = value
    row.data = new_data
    row.modified_by = request.user
    row.save()
    return Response({'success': True})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summary_metrics(request):
    total = DataRow.objects.count()
    live = DataRow.objects.filter(status='Live').count()
    oos = DataRow.objects.filter(status='Out of Stock').count()
    fetch_err = DataRow.objects.filter(status='Fetch Error').count()
    return Response({
        'total_items': total,
        'in_stock': live,
        'out_of_stock': oos,
        'fetch_error': fetch_err
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file_api(request):
    from .views import upload_file
    return upload_file(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_oos(request):
    if request.user.role not in ['Admin', 'Editor']:
        return Response({'error': 'Permission denied'}, status=403)
    rows = DataRow.objects.filter(status='Out of Stock')
    count = rows.count()
    for row in rows:
        Trash.objects.create(original_row_id=row.id, data=row.data, deleted_by=request.user)
        row.delete()
    return Response({'message': f'Moved {count} Out of Stock items to trash'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_fetch_error(request):
    if request.user.role not in ['Admin', 'Editor']:
        return Response({'error': 'Permission denied'}, status=403)
    rows = DataRow.objects.filter(status='Fetch Error')
    count = rows.count()
    for row in rows:
        Trash.objects.create(original_row_id=row.id, data=row.data, deleted_by=request.user)
        row.delete()
    return Response({'message': f'Moved {count} Fetch Error items to trash'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_row(request, item_id):
    if request.user.role not in ['Admin', 'Editor']:
        return Response({'error': 'Permission denied'}, status=403)
    row = get_object_or_404(DataRow, id=item_id)
    Trash.objects.create(original_row_id=row.id, data=row.data, deleted_by=request.user)
    row.delete()
    return Response({'message': 'Item deleted'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_all_data(request):
    if request.user.role not in ['Admin', 'Editor']:
        return Response({'error': 'Permission denied'}, status=403)
    DataRow.objects.all().delete()
    return Response({'message': 'All data cleared'})
