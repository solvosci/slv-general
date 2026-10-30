/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { AITicketDeduplicationItem } from "./AITicketDeduplicationItem";
import { AITicketDeduplicationButtonLoader } from "./AITicketDeduplicationButtonLoader";
import { AITicketSyncButtonLoader } from "./AITicketSyncButtonLoader";

export class AITicketDeduplicationPanel extends Component {
    static template = "helpdesk_ai_ticket_semantic_deduplication.AITicketDeduplicationPanel";
    static components = { AITicketDeduplicationButtonLoader, AITicketDeduplicationItem, AITicketSyncButtonLoader };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.user = useService("user");
        this.state = useState({
            tickets: [],
            isLoading: false,
            hasSearched: false,
            error: "",
            isSyncing: false,
            syncError: "",
        });
        onWillStart(async () => {
            this.canSync = await this.user.hasGroup("helpdesk_mgmt.group_helpdesk_manager");
        });
    }

    async onClick() {
        if (this.state.isLoading) {
            return;
        }
        this.state.isLoading = true;
        this.state.error = "";
        try {
            const result = await this.orm.call(
                "helpdesk.ticket.semantic.context.api.client",
                "request_semantic_context",
                [this.props.record.data.description, 10]
            );
            this.state.tickets = result.tickets;
            this.state.hasSearched = true;
        } catch (error) {
            this.state.error = error.data?.message || _t("Could not search for similar tickets. Please try again.");
        } finally {
            this.state.isLoading = false;
        }
    }

    async onSyncClick() {
        if (this.state.isSyncing) {
            return;
        }
        this.state.isSyncing = true;
        this.state.syncError = "";
        try {
            await this.orm.call("helpdesk.ticket.db.loader.api.client", "load_tickets_db", []);
            this.notification.add(_t("Tickets synchronized with the similarity index."), { type: "success" });
        } catch (error) {
            this.state.syncError = error.data?.message || _t("Could not synchronize tickets. Please try again.");
        } finally {
            this.state.isSyncing = false;
        }
    }
}

registry.category("view_widgets").add("ai_ticket_deduplication_panel", {
    component: AITicketDeduplicationPanel,
});
