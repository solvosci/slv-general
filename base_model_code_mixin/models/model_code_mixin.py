# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ModelCodeMixin(models.AbstractModel):
    _name = "model.code.mixin"

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    is_default = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    complete_name = fields.Char(compute="_compute_complete_name", store=True)
    display_name = fields.Char(compute="_compute_display_name")

    def copy(self, default=None):
        raise ValidationError(_("Copy is disabled"))

    def name_get(self):
        return [(record.id, record.complete_name) for record in self]

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        names1 = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        names2 = []
        if name:
            domain = [("code", "=ilike", name + "%")]
            names2 = self.search(domain, limit=limit).name_get()
        return list(set(names1) | set(names2))[:limit]

    @api.depends("name", "code")
    def _compute_complete_name(self):
        for record in self:
            record.complete_name = "[%s] %s" % (record.code, record.name)

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.complete_name

    @api.constrains("code")
    def _check_code(self):
        for record in self:
            if len(record.search([("code", "=", record.code)])) > 1:
                raise ValidationError(
                    _("Code %s already exists!") % record.code
                )

    @api.constrains("is_default")
    def _check_is_default(self):
        if self.filtered(lambda x: x.is_default):
            if len(self.search([("is_default", "=", True)])) > 1:
                raise ValidationError(
                    _("Only a record could be the default one!")
                )

    @api.model
    def get_default(self):
        return self.search([("is_default", "=", True)])
