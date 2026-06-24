import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DataRow

@login_required
def csv_report(request):
    rows = DataRow.objects.all().values('data')
    data_list = [r['data'] for r in rows]
    df = pd.DataFrame(data_list)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=stock_report.csv'
    df.to_csv(path_or_buf=response, index=False)
    return response

@login_required
def excel_report(request):
    rows = DataRow.objects.all().values('data')
    data_list = [r['data'] for r in rows]
    df = pd.DataFrame(data_list)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Stock')
        
        total = len(df)
        in_stock = DataRow.objects.filter(status='In Stock').count()
        out_of_stock = DataRow.objects.filter(status='Out of Stock').count()
        
        summary = pd.DataFrame({
            'Metric': ['Total Items', 'In Stock', 'Out of Stock'],
            'Count': [total, in_stock, out_of_stock]
        })
        summary.to_excel(writer, sheet_name='Summary', index=False)
    
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=stock_report.xlsx'
    return response

@login_required
def pdf_report(request):
    rows = DataRow.objects.all()
    total = rows.count()
    in_stock = rows.filter(status='In Stock').count()
    out_of_stock = rows.filter(status='Out of Stock').count()
    now_str = timezone.now().strftime('%Y-%m-%d %H:%M')
    
    html_content = '<html><head><title>Stock Report</title>'
    html_content += '<style>body{font-family:Arial}table{border-collapse:collapse;width:100%}'
    html_content += 'th,td{border:1px solid #ddd;padding:8px}th{background:#4CAF50;color:white}</style>'
    html_content += '</head><body><h1>Stock Report</h1>'
    html_content += '<p>Generated: ' + now_str + '</p>'
    html_content += '<p>Total: ' + str(total) + ' | In Stock: ' + str(in_stock) + ' | Out of Stock: ' + str(out_of_stock) + '</p>'
    html_content += '<table><tr><th>Product</th><th>Stock</th><th>Status</th></tr>'
    
    for row in rows:
        product = str(row.data.get('Product', 'N/A'))
        stock = str(row.data.get('Stock', 'N/A'))
        status = str(row.status)
        html_content += '<tr><td>' + product + '</td><td>' + stock + '</td><td>' + status + '</td></tr>'
    
    html_content += '</table></body></html>'
    
    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename=stock_report.html'
    return response
