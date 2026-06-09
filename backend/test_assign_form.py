import asyncio
import uuid
from app.main import app
from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.schemas.user import UserRead
from fastapi.testclient import TestClient

# Mock User
mock_user_id = uuid.uuid4()
mock_user = UserRead(
    id=mock_user_id,
    email="test@example.com",
    full_name="Test User",
    logo_url=None,
    brand_primary_color=None,
    brand_secondary_color=None,
    subscription_tier="solo",
    default_hourly_rate_cents=10000,
    notification_email_prefs={}
)

app.dependency_overrides[get_current_user] = lambda: mock_user

client = TestClient(app)

from app.models.project import Project
from app.models.form_template import FormTemplate
from app.models.client import Client
from app.database import AsyncSessionLocal
import datetime

async def run_test():
    print("Setting up test data...")
    project_id = uuid.uuid4()
    template_id = uuid.uuid4()
    client_id = uuid.uuid4()
    
    async with AsyncSessionLocal() as db:
        db_client = Client(id=client_id, user_id=mock_user_id, name="Test Client", email="client@test.com", portal_token=uuid.uuid4())
        db.add(db_client)
        db_project = Project(id=project_id, user_id=mock_user_id, client_id=client_id, name="Test Project", status="active", description="Test")
        db.add(db_project)
        db_template = FormTemplate(id=template_id, user_id=mock_user_id, name="Test Template")
        db.add(db_template)
        await db.commit()

    print("Sending request to assign form...")
    response = client.post(
        f"/api/v1/projects/{project_id}/forms",
        json={
            "form_template_id": str(template_id),
            "title": "My Form"
        }
    )
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    asyncio.run(run_test())
