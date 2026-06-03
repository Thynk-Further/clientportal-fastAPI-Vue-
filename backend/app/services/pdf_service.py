from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.models.approval import Approval
from typing import List

def generate_approval_history_pdf(approvals: List[Approval], deliverable_name: str) -> BytesIO:
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']
    
    elements = []
    
    elements.append(Paragraph(f"Approval Audit Trail: {deliverable_name}", title_style))
    elements.append(Spacer(1, 12))
    
    data = [['Date', 'Action', 'IP Address', 'Comment']]
    
    for approval in approvals:
        data.append([
            approval.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
            approval.action.upper(),
            approval.client_ip or "Unknown",
            Paragraph(approval.comment or "-", normal_style)
        ])
        
    t = Table(data, colWidths=[110, 100, 100, 160])
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(t)
    
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
