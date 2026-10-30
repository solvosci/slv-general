import requests
from odoo import _, api, models
from odoo.exceptions import AccessError, UserError

class HelpdeskTicketDbLoaderAPiClient(models.AbstractModel):
    _name = "helpdesk.ticket.db.loader.api.client"
    _description = "Helpdesk Ticket DB Loader API Client"

    @api.model
    def _get_db_loader_api_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('helpdesk_ai_ticket_semantic_deduplication.db_loader_api_url')

    @api.model
    def load_tickets_db(self):
        if not self.env.user.has_group('helpdesk_mgmt.group_helpdesk_manager'):
            raise AccessError(_("Only Helpdesk Managers can synchronize tickets."))
        db_loader_api_url = self._get_db_loader_api_url()
        if not db_loader_api_url:
            raise UserError(_("DB Loader API URL not configured. Please configure it in the settings."))
        try:
            response = requests.post(db_loader_api_url, json={'database': self.env.cr.dbname}, timeout=(10, 300))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise UserError(_("Error calling DB Loader API: %s") % str(e))

