from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Trash
from apps.inventory.models import DataRow
from apps.inventory.middleware import AuditLogMiddleware
from apps.accounts.decorators import role_required

@login_required
def trash_list(request):
    return render(request, 'trash/list.html')

@login_required
@role_required(['Admin'])
def auto_remove_oos(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    oos_rows = DataRow.objects.filter(status='Out of Stock')
    count = oos_rows.count()
    
    for row in oos_rows:
        Trash.objects.create(
            original_row_id=row.id,
            data=row.data,
            deleted_by=request.user
        )
        row.delete()
    
    return JsonResponse({'message': f'{count} rows moved to trash'})

@login_required
@role_required(['Admin', 'Editor'])
def restore_item(request, trash_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        trash_item = Trash.objects.get(id=trash_id, restored=False)
    except Trash.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
    DataRow.objects.create(
        data=trash_item.data,
        status='In Stock',
        modified_by=request.user
    )
    
    trash_item.restored = True
    trash_item.save()
    
    return JsonResponse({'message': 'Item restored'})
