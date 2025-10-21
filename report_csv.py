from odoo import http
from odoo.http import request, content_disposition
import csv
import io

class InventoryReportCSVController(http.Controller):
    @http.route('/download/inventory_report/<int:report_id>', type='http', auth='user')
    def download_inventory_report(self, report_id, **kwargs):
        report = request.env['simple.inventory.report'].sudo().browse(report_id)
        if not report.exists():
            return request.not_found()

        output = io.StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        # Nagłówki kolumn
        writer.writerow([
            'Nazwa raportu',
            'Data',
            'Opis',
            'Odpowiedzialny',
            'Laczna ilosc',
            'Laczna wartosc',
            'Lista produktow'
        ])
        products_list = []
        for product in report.product_ids:
            products_list.append(
                f"{product.name}[{product.qty_available},{product.list_price}]"
            )
        # Główne dane raportu
        writer.writerow([
            report.name,
            report.date.strftime('%Y-%m-%d') if report.date else '',
            report.description or '', 
            report.responsible_person.name if report.responsible_person else '',
            str(report.total_quantity).replace('.', ','),
            str(report.total_value).replace('.', ','),
            '|'.join(products_list)  # Produkty oddzielone pionową kreską
        ])

        csv_data = output.getvalue().encode('utf-8')
        output.close()

        filename = kwargs.get('filename', f"raport_{report.id}.csv")
        
        headers = [
            ('Content-Type', 'text/csv; charset=utf-8'),
            ('Content-Disposition', content_disposition(filename))
        ]
        return request.make_response(csv_data, headers)