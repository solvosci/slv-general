# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
{
    'name': 'Scale',
    'author': 'Solvos',
    'category': 'Tools',
    'summary': 'Adds a basic scale management',
    'website': 'https://github.com/solvosci/slv-general',
    'license': 'LGPL-3',
    'version': '13.0.1.0.0',
    'depends': ['uom'],
    'data': [
        'data/scale_data.xml',
        'security/scale_security.xml',
        'security/ir.model.access.csv',
        'views/scale_actions.xml',
        'views/scale_views.xml',
    ],
}
