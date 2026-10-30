{
    "name": "Helpdesk AI Ticket Deduplication",
    "version": "17.0.1.0.0",
    "category": "Helpdesk",
    "summary": "AI-powered ticket creation and semantic duplicate detection",
    "description": """
        Extends OCA Helpdesk Management with AI-powered ticket creation
        and contextual similarity detection.

        Identifies potentially duplicate or related tickets using
        semantic similarity, helping support teams reduce duplication
        and improve ticket management efficiency.
        """,
    "author": "Solvos",
    "website": "https://github.com/solvosci",
    "license": "LGPL-3",
    "depends": [
        "helpdesk_mgmt",
    ],
    "data": [
        "data/ir_config_parameter.xml",
        "views/ticket_form_deduplication.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "helpdesk_ai_ticket_semantic_deduplication/static/src/scss/ticket_deduplication.scss",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/js/SimilarityScoreBadge.js",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/js/AITicketDeduplicationItem.js",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/js/AITicketDeduplicationButtonLoader.js",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/js/AITicketSyncButtonLoader.js",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/js/AITicketDeduplicationPanel.js",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/xml/similarity_score_badge.xml",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/xml/ai_ticket_deduplication_item.xml",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/xml/ai_ticket_deduplication_button_loader.xml",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/xml/ai_ticket_sync_button_loader.xml",
            "helpdesk_ai_ticket_semantic_deduplication/static/src/xml/ai_ticket_deduplication_panel.xml",
        ]
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
