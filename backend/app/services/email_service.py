import resend
from app.config import settings

resend.api_key = settings.RESEND_API_KEY

def send_magic_link(email: str, portal_url: str, client_name: str, freelancer_name: str) -> None:
    try:
        params = {
            "from": f"{freelancer_name} <onboarding@resend.dev>",
            "to": [email],
            "subject": f"Your project portal with {freelancer_name} is ready",
            "html": f"""
            <p>Hi {client_name},</p>
            <p>{freelancer_name} has invited you to their client portal to collaborate on your projects.</p>
            <p>Click the link below to access your portal (no password required):</p>
            <p><a href="{portal_url}">{portal_url}</a></p>
            <p>This link is unique to you. Do not share it.</p>
            """
        }
        
        if resend.api_key and resend.api_key.startswith("re_") and "replace_me" not in resend.api_key:
            email_response = resend.Emails.send(params)
            print(f"Sent email via Resend to {email}. ID: {email_response.get('id', 'unknown')}")
        else:
            print(f"MOCK EMAIL: Would have sent magic link to {email}: {portal_url}")
            
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

def send_notification_email(email: str, recipient_name: str, title: str, message: str, link_url: str = None) -> None:
    try:
        link_html = f'<p><a href="{link_url}">View details</a></p>' if link_url else ""
        params = {
            "from": "ClientPortal <notifications@resend.dev>",
            "to": [email],
            "subject": title,
            "html": f"""
            <p>Hi {recipient_name},</p>
            <p>{message}</p>
            {link_html}
            """
        }
        
        if resend.api_key and resend.api_key.startswith("re_") and "replace_me" not in resend.api_key:
            email_response = resend.Emails.send(params)
            print(f"Sent notification email to {email}. ID: {email_response.get('id', 'unknown')}")
        else:
            print(f"MOCK EMAIL: Would have sent notification to {email}: {title}")
            
    except Exception as e:
        print(f"Failed to send notification email to {email}: {e}")
