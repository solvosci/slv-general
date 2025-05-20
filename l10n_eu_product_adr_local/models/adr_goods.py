# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from odoo.osv.expression import AND
import re


class AdrGoods(models.Model):
    _inherit = 'adr.goods'

    un_local_code = fields.Char(string="UN Code")
    packaging_group_id = fields.Many2one(
        comodel_name='adr.goods.packaging.group',
    )
    _sql_constraints = [
        (
            "un_local_code_uniq",
            "unique(un_local_code)",
            "A Dangerous Good with the same UN local code already exists!",
        )
    ]
    package_description = fields.Text(string="Package Description")

    #  *** This field is used to store NAME of ADR goods without description ***
    clean_name = fields.Char("Clean ADR Name", compute='_compute_clean_name')

    @api.depends('name')
    def _compute_clean_name(self):
        for record in self:
            pattern = r'([A-Z ]+)(?:\s*\([^)]*\))?'
            matches = re.findall(pattern, record.name or '')
            record.clean_name = ' or '.join([m.strip() for m in matches if m.strip()])

    # ***************************************************************************

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = list(args or [])
        if name and operator in ("ilike", "="):
            record = self.search(
                AND([args, [("un_local_code", operator, name)]]), limit=limit
            )
            if record:
                return [(rec.id, rec.display_name) for rec in record]
        return super().name_search(name=name, args=args, operator=operator, limit=limit)

    @api.depends("un_local_code")
    def _compute_display_name(self):
        super()._compute_display_name()
        for rec in self.filtered(lambda r: r.un_local_code):
            rec.display_name = f"{rec.un_local_code} - {rec.display_name}"
