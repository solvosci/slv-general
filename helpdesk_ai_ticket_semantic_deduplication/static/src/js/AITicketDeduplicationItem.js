/** @odoo-module **/
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { SimilarityScoreBadge } from "./SimilarityScoreBadge";

export class AITicketDeduplicationItem extends Component {
    static template = "helpdesk_ai_ticket_semantic_deduplication.AITicketDeduplicationItem";
    static components = { SimilarityScoreBadge };

    setup() {
        this.action = useService("action");
    }

    openTicket() {
        return this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "helpdesk.ticket",
            res_id: this.props.ticket.id,
            views: [[false, "form"]],
            target: "current",
        });
    }

    static props = {
        ticket: {
            type: Object,
            shape: {
                id: Number,
                name: String,
                number: [String, { value: null }],
                description: { type: String, optional: true },
                stage: { type: [String, { value: null }], optional: true },
                similarity: Number,
            },
        },
    };
}
