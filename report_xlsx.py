import io
import xlsxwriter
from odoo import http
from odoo.http import request, content_disposition

class InventoryReportXLSXController(http.Controller):
    
    @http.route('/download/inventory_report_xlsx/<int:report_id>', type='http', auth="user")
    def download_inventory_report_xlsx(self, report_id, **kwargs):
        report = request.env['simple.inventory.report'].sudo().browse(report_id)
        if not report.exists():
            return request.not_found()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Raport Magazynowy')

        # Formatowanie
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#F7F7F7',
            'border': 1,
            'text_wrap': True
        })
        
        bold_format = workbook.add_format({'bold': True})
        currency_format = workbook.add_format({'num_format': '#,##0.00 zł'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

        # Nagłówek raportu
        sheet.merge_range('A1:E1', 'Raport Magazynowy - Podsumowanie', header_format)
        
        # Dane podstawowe
        sheet.write(2, 0, 'Nazwa raportu:', bold_format)
        sheet.write(2, 1, report.name)
        
        sheet.write(3, 0, 'Data:', bold_format)
        sheet.write(3, 1, report.date, date_format)
        
        sheet.write(4, 0, 'Opis:', bold_format)
        sheet.write(4, 1, report.description or '')
        
        sheet.write(5, 0, 'Odpowiedzialny:', bold_format)
        sheet.write(5, 1, report.responsible_person.name or '')
        
        sheet.write(6, 0, 'Łączna ilość:', bold_format)
        sheet.write(6, 1, report.total_quantity)
        
        sheet.write(7, 0, 'Łączna wartość:', bold_format)
        sheet.write(7, 1, report.total_value, currency_format)

        # Nagłówki produktów
        sheet.write(9, 0, 'Lista produktów', bold_format)
        sheet.write(10, 0, 'Nazwa produktu', header_format)
        sheet.write(10, 1, 'Ilość dostępna', header_format)
        sheet.write(10, 2, 'Cena sprzedaży', header_format)
        sheet.write(10, 3, 'Wartość', header_format)
        # Dane produktów
        row = 11
        for product in report.product_ids:
            sheet.write(row, 0, product.name)
            sheet.write(row, 1, product.qty_available)
            sheet.write(row, 2, product.list_price, currency_format)
            sheet.write(row, 3, product.qty_available * product.list_price, currency_format)
            row += 1
        # Dostosowanie szerokości kolumn
        sheet.set_column('A:A', 30)
        sheet.set_column('B:D', 15)
        workbook.close()
        output.seek(0)
        filename = kwargs.get('filename', f"Raport_Magazynowy_{report.name}.xlsx")   
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', content_disposition(filename))
            ]
        )