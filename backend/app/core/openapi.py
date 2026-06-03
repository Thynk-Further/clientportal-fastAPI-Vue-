from fastapi.openapi.utils import get_openapi

openapi_tags = [
    {
        "name": "auth",
        "description": "Freelancer registration, login, token refresh, and client portal session validation",
    },
    {
        "name": "users",
        "description": "Freelancer profile and branding management",
    },
    {
        "name": "clients",
        "description": "Client management and portal link generation",
    },
    {
        "name": "projects",
        "description": "Project lifecycle management",
    },
    {
        "name": "deliverables",
        "description": "Deliverable management within projects",
    },
    {
        "name": "files",
        "description": "Presigned upload URLs and file metadata",
    },
    {
        "name": "approvals",
        "description": "Append-only approval audit trail and PDF export",
    },
    {
        "name": "messages",
        "description": "REST history fetch for project and deliverable threads",
    },
    {
        "name": "time-entries",
        "description": "Time tracking: manual entries and live timer",
    },
    {
        "name": "forms",
        "description": "Form template builder and submission management",
    },
    {
        "name": "invoices",
        "description": "Invoice creation, sending, and Stripe integration",
    },
    {
        "name": "portal",
        "description": "Client-facing portal endpoints (session-cookie auth)",
    },
    {
        "name": "webhooks",
        "description": "Stripe webhook event handling",
    },
]
