/** @odoo-module **/
import { Component } from "@odoo/owl";

export class AITicketSyncButtonLoader extends Component {
    static template = "helpdesk_ai_ticket_semantic_deduplication.AITicketSyncButtonLoader";
    static props = {
        isLoading: { type: Boolean, optional: true },
        onClick: Function,
    };
}
