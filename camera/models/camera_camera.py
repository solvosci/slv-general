# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields
from odoo.exceptions import UserError

import requests
import base64


class Camera(models.Model):
    _name = 'camera.camera'
    _description = "Camera"

    name = fields.Char(required=True)
    url = fields.Char(required=True)
    refresh_time = fields.Integer(default=1000, required=True, help='Time in ms')
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
    )
    last_image = fields.Image(copy=False, readonly=True)
    last_image_mini = fields.Image(
        "Variant Image Mini",
        related="last_image",
        max_width=92,
        max_height=92,
        store=True,
    )
    active = fields.Boolean(default=True)

    def get_image(self):
        self.ensure_one()
        try:
            img_data = requests.get(self.url.strip()).content
        except requests.exceptions.ConnectionError as err:
            raise UserError(err)

        self.last_image = base64.b64encode(img_data).replace(b'\n', b'')
