"""
Improved PDF generation that attempts to preserve more of the original formatting.

While true in-place PDF editing is extremely difficult (PDFs are not designed for editing),
this version captures more style information during extraction and recreates it more faithfully.

For production, consider these alternatives:
1. PDF → DOCX conversion → edit → PDF (using tools like pdf2docx)
2. Encourage users to upload DOCX instead of PDF for best results
3. Use specialized PDF editing libraries (e.g., PyPDF2 with ReportLab overlay)
"""
import logging
from typing import Dict, List

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

logger = logging.getLogger(__name__)


def _get_alignment(style_name: str, text: str) -> int:
    """Infer text alignment"""
    # Center if short and looks like a heading
    if len(text) < 50 and text.isupper():
        return TA_CENTER
    return TA_LEFT


def _create_paragraph_style(para_info: dict, base_style: ParagraphStyle) -> ParagraphStyle:
    """
    Create a paragraph style based on extracted formatting information.
    Preserves font size, bold, italic, and color where available.
    """
    runs = para_info.get("runs", [])
    
    if not runs:
        return base_style
    
    # Use the first run's style as the primary style
    first_run = runs[0]
    run_style = first_run.get("style", {})
    
    # Extract style properties
    font_size = run_style.get("size_pt", base_style.fontSize)
    is_bold = run_style.get("bold", False)
    is_italic = run_style.get("italic", False)
    color = run_style.get("color")
    
    # Determine font name
    if is_bold and is_italic:
        font_name = "Helvetica-BoldOblique"
    elif is_bold:
        font_name = "Helvetica-Bold"
    elif is_italic:
        font_name = "Helvetica-Oblique"
    else:
        font_name = "Helvetica"
    
    # Create custom style
    style = ParagraphStyle(
        name=f"Custom_{para_info.get('para_index', 0)}",
        parent=base_style,
        fontName=font_name,
        fontSize=font_size if font_size else base_style.fontSize,
        leading=font_size * 1.2 if font_size else base_style.leading,
        spaceAfter=base_style.spaceAfter,
        alignment=_get_alignment(para_info.get("style_name", ""), para_info.get("text", ""))
    )
    
    # Apply color if available
    if color and color != "None":
        try:
            style.textColor = HexColor(f"#{color}")
        except:
            pass  # Use default color on error
    
    return style


def render(sections: List[dict], changes: List[dict], output_path: str) -> None:
    """
    Render enhanced resume to PDF with better formatting preservation.
    
    Captures and applies:
    - Font sizes from original
    - Bold/italic formatting
    - Colors
    - Better heading detection and styling
    """
    try:
        logger.info(f"Rendering PDF to {output_path}")
        
        # Create change index for fast lookup
        by_index = {c["para_index"]: c["after"] for c in changes}
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Create default styles
        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=HexColor("#2C3E50"),
            spaceAfter=8,
            spaceBefore=12,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            "CustomBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            spaceAfter=6,
            alignment=TA_LEFT
        )
        
        # Process each section
        for section_idx, section in enumerate(sections):
            heading = section["heading"]
            
            # Skip or format preamble (contact info) specially
            if heading == "PREAMBLE":
                # Center-align contact information
                for para in section["paragraphs"]:
                    text = by_index.get(para["para_index"], para["text"])
                    preamble_style = ParagraphStyle(
                        "Preamble",
                        parent=body_style,
                        alignment=TA_CENTER,
                        fontSize=10,
                        spaceAfter=3
                    )
                    story.append(Paragraph(text, preamble_style))
                story.append(Spacer(1, 12))
                continue
            
            # Add section heading
            story.append(Paragraph(heading, heading_style))
            
            # Add paragraphs with preserved formatting
            for para in section["paragraphs"]:
                # Get enhanced text if available
                text = by_index.get(para["para_index"], para["text"])
                
                # Create style based on original formatting
                para_style = _create_paragraph_style(para, body_style)
                
                # Handle bullet points
                if text.strip().startswith(('•', '-', '*', '·')):
                    # Add slight indent for bullets
                    para_style = ParagraphStyle(
                        name=para_style.name + "_bullet",
                        parent=para_style,
                        leftIndent=15,
                        bulletIndent=5
                    )
                
                story.append(Paragraph(text, para_style))
            
            # Add spacing between sections
            story.append(Spacer(1, 10))
        
        # Build PDF
        doc.build(story)
        logger.info("PDF rendering complete")
    
    except Exception as e:
        logger.error(f"Error rendering PDF: {e}", exc_info=True)
        raise


def render_with_comparison(original_sections: List[dict], enhanced_sections: List[dict], 
                          changes: List[dict], output_path: str) -> None:
    """
    Render a side-by-side comparison PDF showing original vs enhanced.
    Useful for premium users who want to see detailed changes.
    """
    # TODO: Implement side-by-side comparison view
    # This would require table layout with two columns
    pass
