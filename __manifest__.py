{
    'name': 'raporty_stan_magazynu',
    'author': "justyna",
    'description': 'Moduł do generowania raportów magazynowych',
    'version': '0.1',
    'category': 'Warehouse',
    'summary': 'Modul do generowania raportów',
    'depends': ['base','stock','product','web'],
    'license': 'LGPL-3',
    'data': [
        'security/simple_inventory_report_model.xml',
        'security/ir.model.access.csv',  
        'views/raport_menu.xml',  
      
    ],
    'installable': True,
    'application': True,
    
}