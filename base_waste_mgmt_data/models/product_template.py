# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    low_code = fields.Char(string="LoW Code")
