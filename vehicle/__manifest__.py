# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
{
    'name': 'Vehicle',
    'author': 'Solvos',
    'category': 'Human Resources/Fleet',
    'summary': 'Vehicle',
    'website': 'https://github.com/solvosci/slv-general',
    'license': 'LGPL-3',
    'version': '13.0.1.0.2',
    'depends': [
        'mail',
        'portal',
    ],
    'data': [
        'data/vehicle.xml',
        'security/vehicle.xml',
        'security/ir.model.access.csv',
        'views/vehicle_menu.xml',
        'views/vehicle_views.xml',
    ],
    'application': True,
}
