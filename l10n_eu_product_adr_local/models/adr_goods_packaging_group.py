# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class AdrGoodsPackagingGroup(models.Model):
    _name = 'adr.goods.packaging.group'
    _description = 'Packaging ADR Good group'

    name = fields.Char(required=True)
    description = fields.Text()
    maximum_capacity = fields.Float()
    multiplier = fields.Float()
