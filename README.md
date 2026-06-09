<img width="1806" height="929" alt="Screenshot 2026-06-09 110655" src="https://github.com/user-attachments/assets/c9c01646-0c17-4d41-95c4-f4801a41bd5f" />
<img width="1775" height="928" alt="Screenshot 2026-06-09 110628" src="https://github.com/user-attachments/assets/afce07b3-b006-4df0-af76-f15c1e0b9cae" />
<img width="1802" height="927" alt="Screenshot 2026-06-09 110554" src="https://github.com/user-attachments/assets/a83c2d6e-8ede-4dab-86c9-7e6ee0169dd5" />
<img width="1798" height="933" alt="Screenshot 2026-06-09 110530" src="https://github.com/user-attachments/assets/3f0c782a-2485-47f9-8b5f-75960659b615" />
<img width="1792" height="945" alt="Screenshot 2026-06-09 110401" src="https://github.com/user-attachments/assets/5f91f2db-cbd2-4199-9e77-a195d063a631" />
<img width="1782" height="895" alt="Screenshot 2026-06-09 103358" src="https://github.com/user-attachments/assets/35b87689-0caa-4818-8152-d70f63931205" />
<img width="1812" height="929" alt="Screenshot 2026-06-09 103331" src="https://github.com/user-attachments/assets/3cba816a-708c-4e8c-ad74-1ec62cfd2da0" />
<img width="1821" height="923" alt="Screenshot 2026-06-09 103249" src="https://github.com/user-attachments/assets/3c0eb9a4-c331-4a35-a464-487d7a90fe35" />
<img width="1784" height="946" alt="Screenshot 2026-06-09 103227" src="https://github.com/user-attachments/assets/ec5b9333-1e6b-457b-a094-78381a26381b" />
<img width="1806" height="928" alt="Screenshot 2026-06-09 103201" src="https://github.com/user-attachments/assets/33ba52be-b9dd-46a0-9ded-f67fc4fc1fde" />
<img width="1813" height="927" alt="Screenshot 2026-06-09 101843" src="https://github.com/user-attachments/assets/dc69bc51-a303-4def-9da2-9111d8eaec9f" />
<img width="1805" height="922" alt="Screenshot 2026-06-09 101825" src="https://github.com/user-attachments/assets/35b82630-9177-414c-9352-42340822e8c4" />
<img width="1790" height="915" alt="Screenshot 2026-06-09 101803" src="https://github.com/user-attachments/assets/a38cb047-3fed-4c48-bfb4-f8fee5e48e65" />
<img width="1809" height="941" alt="Screenshot 2026-06-09 101735" src="https://github.com/user-attachments/assets/45a24e7d-6a4e-472f-aa3e-903c84e41497" />
<img width="1910" height="979" alt="Screenshot 2026-06-09 101659" src="https://github.com/user-attachments/assets/cb9b2075-6f42-4e4e-8801-ed314fc6cdbc" />
<img width="1784" height="901" alt="Screenshot 2026-06-09 101535" src="https://github.com/user-attachments/assets/432b7f7b-3a47-40ed-9892-8f152c7692ea" />
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
