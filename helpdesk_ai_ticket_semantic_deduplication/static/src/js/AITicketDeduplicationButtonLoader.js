/** @odoo-module **/
import { Component } from "@odoo/owl";

export class AITicketDeduplicationButtonLoader extends Component {
    static template = "helpdesk_ai_ticket_semantic_deduplication.AITicketDeduplicationButtonLoader";
    static props = {
        isLoading: { type: Boolean, optional: true },
        onClick: Function,
    };
}
