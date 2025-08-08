# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
from odoo import fields, models, exceptions, _, api


class Vehicle(models.Model):
    _name = "vehicle.vehicle"
    _description = "Vehicle"
    _inherit = ["mail.thread.cc", "mail.activity.mixin"]

    name = fields.Char(
        compute="_compute_name",
        store=True
    )
    license_plate = fields.Char(
        index=True,
        required=True,
        copy=False,
        tracking=True,
    )
    active = fields.Boolean(string="Active", default=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible user",
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
    )
    has_group_vehicle_manager = fields.Boolean(compute="_compute_has_group_vehicle_manager")

    _sql_constraints = [(
        "license_plate",
        "unique(license_plate)",
        "The license plate must be unique!"
    )]

    @api.depends('license_plate')
    def _compute_name(self):
        for record in self:
            record.name = record.license_plate

    @api.returns('self', lambda value: value.id)
    def copy(self):
        raise exceptions.UserError(_('You cannot duplicate a vehicle.'))

    @api.depends('license_plate')
    def _compute_has_group_vehicle_manager(self):
        group = "vehicle.group_vehicle_manager"
        for record in self:
            record.has_group_vehicle_manager = self.env.user.has_group(group) | False
