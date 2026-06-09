# ClientPortal

ClientPortal is a highly focused, purpose-built client portal for freelancers. It provides an all-in-one space to share deliverables, collect timestamped approvals, track time, host project discussions, manage forms/questionnaires, and get paid—without the setup overhead of heavy, all-in-one tools like Dubsado or HoneyBook.

The platform is built as a unified monorepo divided into two audience domains:
1. **Freelancer Dashboard**: A secure space (protected by JWT access and refresh tokens) for freelancers to manage clients, projects, deliverables, invoices, and templates.
2. **Client Portal**: A frictionless, magic-link protected space for clients to review deliverables, pay invoices, and answer forms without needing to create an account or remember a password.

## Architecture & Tech Stack

This repository contains both the Nuxt 3 frontend and the FastAPI backend.

### Frontend
- **Framework**: Nuxt 3 + Vue 3 (Composition API) with TypeScript
- **Styling**: Tailwind CSS + Shadcn-Vue components
- **State Management**: Pinia
- **Dual Layout System**: Distinct layouts (`default.vue` and `portal.vue`) ensuring strict separation between Freelancer and Client contexts.
- **Dynamic Theming**: CSS variables injected at runtime to dynamically apply the freelancer's brand colors to the client's portal.

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL 16 (via async SQLAlchemy 2.0 & Alembic)
- **Validation**: Pydantic v2
- **File Storage**: Cloudflare R2 (S3-compatible, Direct Upload Pattern)
- **Payments**: Stripe (Invoices + Payment Element)
- **Transactional Emails**: Resend
- **Real-Time Communication**: FastAPI WebSockets
- **Document Export**: ReportLab (PDFs)

## Core Features

- **Magic Link Authentication**: Frictionless onboarding. Clients receive an email with a secure, server-generated token to access their portal instantly. The backend issues httpOnly session cookies upon validation.
- **Smart Onboarding Flow**: An interactive "Getting Started" walkthrough grid that guides clients through their first portal visit, tracking progress via local storage and auto-dismissing upon completion.
- **Append-Only Audit Trails**: Approvals are strictly append-only in the database. A full approval history can be exported dynamically as a PDF using ReportLab.
- **File Bypass Uploads**: File uploads (both project deliverables and client form assets) bypass the FastAPI server completely. The API generates short-lived presigned PUT URLs, allowing the browser to upload directly to Cloudflare R2. This keeps the backend stateless.
- **Real-Time Discussions**: Built-in WebSocket integration for live chat and feedback on specific deliverables.
- **Embedded Invoicing**: Native Stripe SDK integration. The API lazily creates Stripe Customers and generates Stripe Invoices. Clients pay seamlessly via the Stripe Payment Element directly from the portal.
- **Time Tracking**: Live timers and manual time entries tied directly to projects, automatically calculating durations and applying project or default hourly rates.
- **Dynamic Forms**: A robust schema for freelancers to create custom questionnaires. Supports partial auto-saves by the client and full server-side validation upon final submission.

## Repository Structure

```
ClientPortal/
├── backend/            # FastAPI Backend
│   ├── app/            # Application logic, routers, models, schemas
│   ├── alembic/        # Database migrations
│   ├── requirements.txt
│   └── ...
├── frontend/           # Nuxt 3 Frontend
│   ├── app/            # Pages, components, composables, layouts
│   ├── nuxt.config.ts
│   ├── package.json
│   └── ...
└── README.md
```

## Local Development Setup

### 1. Requirements
- Python 3.12
- Node.js (v18+)
- PostgreSQL 16 (or SQLite for rapid local testing)

### 2. Backend Setup
Create a `.env` file in the `backend/` directory based on the following template:

```env
DATABASE_URL=sqlite+aiosqlite:///./clientportal.db
SECRET_KEY=your_secret_key
REFRESH_SECRET_KEY=your_refresh_secret
R2_ENDPOINT_URL=https://<account_id>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=clientportal-uploads
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
RESEND_API_KEY=re_...
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```
*(Note: The system contains built-in mock fallbacks for Resend and Stripe if keys are left blank during initial development.)*

Navigate to the `backend/` directory, create a virtual environment, and install dependencies:

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

Start the Uvicorn ASGI server:
```bash
uvicorn app.main:app --reload
```
The Swagger API documentation will be automatically generated and available at `http://127.0.0.1:8000/docs`.

### 3. Frontend Setup
Create a `.env` file in the `frontend/` directory:

```env
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

Navigate to the `frontend/` directory, install Node dependencies, and start the development server:

```bash
cd frontend
npm install
npm run dev
```
The Nuxt application will be running at `http://localhost:3000`.
