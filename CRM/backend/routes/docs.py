import tempfile

from fastapi import APIRouter
from fastapi.responses import FileResponse
try:
    from fpdf import FPDF
except ImportError:  # pragma: no cover - optional dependency
    FPDF = None

router = APIRouter(prefix="/docsgen", tags=["docs"])


@router.post("/generate", summary="Generate document")
def generate_document(name: str):
    if FPDF is None:
        raise RuntimeError("fpdf2 not installed")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(40, 10, text=f"Document: {name}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        tmp_path = tmp.name
    return FileResponse(tmp_path, filename=f"{name}.pdf", media_type="application/pdf")


@router.get("/invoice/export/{invoice_id}", summary="Export invoice as PDF")
def export_invoice(invoice_id: int):
    if FPDF is None:
        raise RuntimeError("fpdf2 not installed")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(40, 10, text=f"Invoice #{invoice_id}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        tmp_path = tmp.name
    return FileResponse(
        tmp_path,
        filename=f"invoice_{invoice_id}.pdf",
        media_type="application/pdf",
    )


@router.get("/report/management", summary="Generate management report")
def management_report():
    if FPDF is None:
        raise RuntimeError("fpdf2 not installed")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(40, 10, text="Management Report")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        tmp_path = tmp.name
    return FileResponse(
        tmp_path, filename="management_report.pdf", media_type="application/pdf"
    )
