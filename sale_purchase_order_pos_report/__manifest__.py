# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Purchase Order Pos Report",
    "summary": """
        Integrates the sale_order_purchase_line_report module with point_of_sale
        enabling tracking and reporting of refunded quantities (refund_qty)
        generated from POS transactions.
    """,
    "version": "17.0.1.0.0",
    "author": "Solvos",
    "category": "Sales/Purchases",
    "license": "LGPL-3",
    "website": "https://github.com/solvosci/slv-general",
    "depends": [
        "sale_purchase_order_line_report",
        "point_of_sale"
        ],
    "data": [
        "views/sale_purchase_order_line_views.xml",
        ]
}
