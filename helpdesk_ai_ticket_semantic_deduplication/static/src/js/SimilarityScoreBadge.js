/** @odoo-module **/
import { Component } from "@odoo/owl";

export class SimilarityScoreBadge extends Component {
    static template = "helpdesk_ai_ticket_semantic_deduplication.SimilarityScoreBadge";

    static props = {
        score: Number,
    };

    get percentage() {
        return Math.round(this.props.score * 100);
    }

    get levelClass() {
        if (this.props.score >= 0.85) {
            return "o_ait_ticket_deduplication_item__score--high";
        }
        if (this.props.score >= 0.6) {
            return "o_ait_ticket_deduplication_item__score--medium";
        }
        return "o_ait_ticket_deduplication_item__score--low";
    }
}
