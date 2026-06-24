import uuid, pandas as pd, traceback, sys
from io import StringIO, BytesIO
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import DataRow
from .middleware import AuditLogMiddleware
from apps.accounts.decorators import role_required

@login_required
def dashboard_view(request):
    return render(request, 'inventory/dashboard.html')

@login_required
@role_required(['Admin', 'Editor'])
def upload_file(request):
    try:
        if request.method != 'POST' or 'file' not in request.FILES:
            return JsonResponse({'error': 'No file'}, status=400)
        file = request.FILES['file']
        fname = file.name.lower()
        if not fname.endswith(('.csv', '.xlsx', '.xls')):
            return JsonResponse({'error': 'Invalid file type'}, status=400)
        content = file.read()
        if fname.endswith('.csv'):
            try:
                df = pd.read_csv(StringIO(content.decode('utf-8')))
            except:
                df = pd.read_csv(StringIO(content.decode('latin-1')))
        else:
            df = pd.read_excel(BytesIO(content), header=None)

        # CLEAR ALL OLD DATA
        DataRow.objects.all().delete()

        batch_id = uuid.uuid4()
        saved = 0

        for idx, row in df.iterrows():
            try:
                status_raw = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
                status_lower = status_raw.lower()

                # skip header/metadata rows
                sku_val = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else ''
                if sku_val in ('', 'nan', 'SKU', 'Shipping') and status_lower in ('', 'nan', 'status', 'vc charges', 'custom'):
                    continue

                if status_lower == 'out of stock':
                    stock_status, reason = 'Out of Stock', 'Out of Stock'
                elif status_lower == 'fetch error':
                    stock_status, reason = 'Fetch Error', 'Fetch Error'
                elif status_lower == 'live':
                    stock_status, reason = 'Live', ''
                else:
                    stock_status, reason = 'Live', ''

                data_dict = {}
                columns = ['Status','SKU','SupplierID','eBayPrice','OurCost','Link',
                           'SalePrice','Profit','GrossMargin','Reference']
                for i, col in enumerate(columns):
                    if i < len(row) and pd.notna(row.iloc[i]):
                        val = row.iloc[i]
                        if isinstance(val, float) and val == int(val):
                            val = int(val)
                        data_dict[col] = str(val)
                    else:
                        data_dict[col] = ''

                sku = data_dict.get('SKU', '').strip()
                if sku and sku.lower() not in ('nan', 'sku', ''):
                    DataRow.objects.create(
                        upload_id=batch_id, row_index=idx,
                        data=data_dict, status=stock_status,
                        reason=reason, modified_by=request.user
                    )
                    saved += 1
            except Exception as e:
                print(f'Row {idx} error: {e}', file=sys.stderr)
                continue

        total = DataRow.objects.count()
        live = DataRow.objects.filter(status='Live').count()
        oos = DataRow.objects.filter(status='Out of Stock').count()
        fetch_err = DataRow.objects.filter(status='Fetch Error').count()

        AuditLogMiddleware.log_action(
            request.user, 'upload', 'DataRow', str(batch_id),
            f'Uploaded {total} rows (Live:{live}, OOS:{oos}, FetchErr:{fetch_err})',
            request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({
            'message': f'Uploaded {total} products (Live: {live}, Out of Stock: {oos}, Fetch Error: {fetch_err})',
            'total': total, 'live': live, 'out_of_stock': oos, 'fetch_error': fetch_err
        })
    except Exception as e:
        print(traceback.format_exc(), file=sys.stderr)
        return JsonResponse({'error': str(e)}, status=500)
