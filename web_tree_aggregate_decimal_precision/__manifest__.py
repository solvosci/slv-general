# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
{
    'name': 'Web Tree Aggregate Decimal Precision',
    'summary': """
        By default, summary totals don't follow the source field’s digits configuration
        and always will show 2 decimals digits.
        This module allows to set the decimal precision of the aggregate values in tree views.
    """,
    'author': 'Solvos',
    'category': 'Tools',
    'website': 'https://github.com/solvosci/slv-general',
    'license': 'LGPL-3',
    'version': '17.0.1.0.0',
    "depends": [
        "web"
    ],
    "assets": {
        "web.assets_backend": [
            "web_tree_aggregate_decimal_precision/static/src/list_renderer_digits_patch.esm.js",
        ],
    },
}
