import requests
from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools import html2plaintext

class HelpdeskTicketSemanticContextApiClient(models.AbstractModel):
    _name = 'helpdesk.ticket.semantic.context.api.client'
    _description = 'Helpdesk Ticket Semantic Context API Client'

    @api.model
    def _get_semantic_context_api_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('helpdesk_ai_ticket_semantic_deduplication.semantic_context_api_url')

    @api.model
    def request_semantic_context(self, description, limit=10):
        semantic_context_api_url = self._get_semantic_context_api_url()
        if not semantic_context_api_url:
            raise UserError(_("Semantic Context API URL not configured. Please configure it in the settings."))
        payload = {
            'database': self.env.cr.dbname,
            'company_id': self.env.company.id,
            'description': html2plaintext(description or ''),
            'limit': limit,
        }
        try:
            response = requests.post(semantic_context_api_url, json=payload, timeout=(10, 60))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise UserError(_("Error calling Semantic Context API: %s") % str(e))
