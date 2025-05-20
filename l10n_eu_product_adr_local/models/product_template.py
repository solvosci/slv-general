# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    un_local_code = fields.Char(
        related='product_variant_ids.adr_goods_id.un_local_code')
    packaging_group_id = fields.Many2one(
        comodel_name='adr.goods.packaging.group',
        related='product_variant_ids.adr_goods_id.packaging_group_id'
    )
