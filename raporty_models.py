from odoo import models, fields, api
from datetime import datetime

class SimpleInventoryReport(models.Model):
    _name = 'simple.inventory.report'
    _description = 'Prosty raport magazynowy'
    
    name = fields.Char(
        string='Nazwa', 
        default=lambda self: "Raport z dnia " + datetime.now().strftime('%Y-%m-%d')
    )
    date = fields.Date(
        string='Data', 
        default=fields.Date.context_today
    )
    description = fields.Text(string='Opis')

    responsible_person = fields.Many2one(
        comodel_name='res.users',
        string='Odpowiedzialny'
    )

    product_ids = fields.Many2many(
        comodel_name='product.product',
        string='Produkty'
    )
    total_quantity = fields.Float(
        string="Łączna ilość (sztuki)",
        compute="_compute_inventory_totals",
        digits=(12, 2)
    )

    total_value = fields.Float(
        string="Łączna wartość (PLN)",
        compute="_compute_inventory_totals",
        digits=(12, 2)
    )

    @api.depends('product_ids')
    def _compute_inventory_totals(self):
        for report in self:
            total_qty = 0.0
            total_val = 0.0
            
            #  aktualizacja stanów magazynowych
            if report.product_ids:
                report.product_ids._compute_quantities()
                
                for product in report.product_ids:
                    qty = product.qty_available
                    price = product.list_price
                    
                    if qty and price:  # Tylko jeśli obie wartości istnieją
                        total_qty += qty
                        total_val += qty * price
            
            # Przypisujemy wartości
            report.total_quantity = total_qty
            report.total_value = total_val


    def download_csv_report(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return {
            'type': 'ir.actions.act_url',
            'url': f'{base_url}/download/inventory_report/{self.id}?filename=Raport_{self.id}.csv',
            'target': 'self',
        }

    def download_xlsx_report(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return {
            'type': 'ir.actions.act_url',
            'url': f'{base_url}/download/inventory_report_xlsx/{self.id}?filename=Raport_{self.id}.xlsx',
            'target': 'self',
        }