# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Purchase Order Line Report",
    "summary": """
        Create a view that combines purchase and sales order lines,
        accessible from both partner and product.
        There are two modes of viewing the view:
        - report on ordered quantities
        - report on received/delivered quantities
        configurable in the settings.
    """,
    "version": "17.0.2.1.0",
    "author": "Solvos",
    "category": "Sales/Purchases",
    "license": "LGPL-3",
    "website": "https://github.com/solvosci/slv-general",
    "depends": ["sale",
                "purchase",
                ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sale_purchase_order_line_views.xml",
        "views/res_partner_views.xml",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
    ]
}
