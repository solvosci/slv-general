# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields, _
from odoo.exceptions import UserError
import requests


class ASM(models.Model):
    _name = 'asm.asm'
    _description = "ASM"

    name = fields.Char(required=True)
    url = fields.Char(required=True)
    refresh_time = fields.Integer(
        default=1000,
        required=True,
        help='Time in ms'
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)

    def get_status(self):
        self.ensure_one()
        try:
            text_html = requests.get(self.url).text
            color_param_1 = text_html.find("<body bgcolor=") + 15
            color_param_2 = color_param_1 + 6
            color = text_html[color_param_1:color_param_2]

            status_param_1 = text_html.find("<h1>") + 4
            status_param_2 = text_html.find("</h1>")
            status = text_html[status_param_1:status_param_2]

            return {
                "color": color,
                "status": status,
                "refresh_time": self.refresh_time
            }
        except requests.exceptions.ConnectionError as err:
            raise UserError(err)

    def test_status(self):
        values = self.get_status()
        msg = (_("Success!!\nColor: %s\nStatus: %s")) % \
            (values["color"], values["status"])
        raise UserError(msg)
