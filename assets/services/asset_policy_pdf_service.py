from io import BytesIO
from pathlib import Path

from django.conf import settings
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


class AssetPolicyPDFService:
    POLICY_PATH = (
        Path(settings.BASE_DIR)
        / "assets"
        / "documents"
        / "Laptop_Policy.pdf"
    )

    @classmethod
    def generate_employee_policy(cls, employee_name: str):
        if not cls.POLICY_PATH.is_file():
            raise FileNotFoundError(
                f"Laptop policy PDF not found: {cls.POLICY_PATH}"
            )

        if not employee_name or not employee_name.strip():
            raise ValueError("Employee name cannot be empty.")

        reader = PdfReader(str(cls.POLICY_PATH))

        if len(reader.pages) < 2:
            raise ValueError(
                "Laptop policy must contain at least two pages."
            )

        # Create a transparent overlay matching page 2.
        page = reader.pages[1]
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        overlay_buffer = BytesIO()
        pdf_canvas = canvas.Canvas(
            overlay_buffer,
            pagesize=(width, height),
        )
        pdf_canvas.setFont("Helvetica", 10)
        pdf_canvas.drawString(105, 389, employee_name.strip())
        pdf_canvas.save()
        overlay_buffer.seek(0)

        overlay_page = PdfReader(overlay_buffer).pages[0]

        writer = PdfWriter()
        for index, source_page in enumerate(reader.pages):
            if index == 1:
                source_page.merge_page(overlay_page)
            writer.add_page(source_page)

        output_buffer = BytesIO()
        writer.write(output_buffer)

        safe_name = "_".join(employee_name.strip().split())
        filename = f"Laptop_Policy_{safe_name}.pdf"

        return filename, output_buffer.getvalue()