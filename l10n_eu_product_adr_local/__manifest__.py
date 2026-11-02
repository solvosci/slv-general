# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "ADR Dangerous Goods Local",
    "summary": """
        Extend ADR Dangerous Goods with local information,
        by adding UN codes and packaging groups.
        Also creates clean_name field,
        used to store NAME of ADR goods without description
    """,
    "version": "17.0.1.0.0",
    "category": "Inventory/Delivery",
    "website": "https://github.com/solvosci/slv-general",
    "author": "Solvos",
    "license": "AGPL-3",
    "depends": ["l10n_eu_product_adr"],
    "development_status": "Beta",
    "data": [
        "security/ir.model.access.csv",
        "views/adr_goods_views.xml",
        "views/adr_goods_packaging_group_views.xml",
        "views/product_template_views.xml"
    ],
}
