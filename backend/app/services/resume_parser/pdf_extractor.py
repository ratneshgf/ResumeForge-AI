"""
Production-grade PDF extraction with enhanced text and formatting capture.

Uses PyMuPDF to extract text blocks with styling information. While PDFs
cannot be edited in-place like DOCX (no editable text runs), this extractor
captures maximum formatting detail for faithful reconstruction.
"""
import logging
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

# Same comprehensive section keywords as DOCX extractor
SECTION_KEYWORDS = {
    "contact", "contact information", "personal information",
    "career objective", "objective", "summary", "professional summary", "profile",
    "experience", "work experience", "professional experience", "employment history",
    "education", "academic background", "qualifications",
    "technical skills", "skills", "core competencies", "expertise",
    "projects", "key projects", "academic projects",
    "certifications", "certificates", "professional certifications",
    "achievements", "accomplishments", "honors", "awards",
}


def _normalize_heading(heading: str) -> str:
    """Normalize heading to standard format"""
    heading_lower = heading.strip(":").strip().lower()
    
    # Map to standard categories
    keyword_map = {
        "contact": "CONTACT",
        "objective": "OBJECTIVE",
        "summary": "OBJECTIVE",
        "experience": "EXPERIENCE",
        "education": "EDUCATION",
        "skills": "SKILLS",
        "projects": "PROJECTS",
        "certifications": "CERTIFICATIONS",
        "achievements": "ACHIEVEMENTS",
    }
    
    for keyword, category in keyword_map.items():
        if keyword in heading_lower:
            return category
    
    return heading.strip()


def _is_heading(text: str, font_size: float, is_bold: bool) -> bool:
    """
    Determine if text is a section heading based on:
    - Font size (larger than typical body text)
    - Bold formatting
    - Matches known section keywords
    """
    text_lower = text.strip(":").lower()
    
    # Check for section keywords
    if any(keyword in text_lower for keyword in SECTION_KEYWORDS):
        return True
    
    # Bold and larger font
    if is_bold and font_size > 11.5:
        return True
    
    # All caps and short
    if text.isupper() and len(text) < 50 and is_bold:
        return True
    
    return False


def extract(path: str) -> dict:
    """
    Extract structured data from PDF with intelligent section detection.
    
    Returns:
        Dictionary with 'sections' key containing list of section dicts
    """
    try:
        logger.info(f"Extracting PDF: {path}")
        
        doc = fitz.open(path)
        sections: list[dict] = []
        current = {"heading": "PREAMBLE", "paragraphs": []}
        para_index = 0
        
        for page_num, page in enumerate(doc):
            logger.debug(f"Processing page {page_num + 1}")
            
            # Extract text with formatting
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                # Skip image blocks
                if block.get("type") != 0:  # 0 = text block
                    continue
                
                for line in block.get("lines", []):
                    # Extract text and spans (character runs)
                    spans = line.get("spans", [])
                    if not spans:
                        continue
                    
                    text = "".join(span["text"] for span in spans).strip()
                    if not text:
                        continue
                    
                    # Analyze formatting
                    font_sizes = [span["size"] for span in spans]
                    max_font_size = max(font_sizes) if font_sizes else 11
                    avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 11
                    
                    # Check if any span is bold
                    any_bold = any("bold" in span["font"].lower() for span in spans)
                    any_italic = any("italic" in span["font"].lower() for span in spans)
                    
                    # Determine if this is a heading
                    is_heading = _is_heading(text, max_font_size, any_bold)
                    
                    if is_heading:
                        # Save previous section
                        if current["paragraphs"]:
                            sections.append(current)
                        
                        # Start new section
                        normalized_heading = _normalize_heading(text)
                        current = {"heading": normalized_heading, "paragraphs": []}
                        logger.debug(f"Detected section heading: {text} -> {normalized_heading}")
                    else:
                        # Add as paragraph
                        current["paragraphs"].append({
                            "para_index": para_index,
                            "style_name": "Normal",
                            "text": text,
                            "runs": [{
                                "run_index": 0,
                                "text": text,
                                "style": {
                                    "bold": any_bold,
                                    "italic": any_italic,
                                    "size_pt": avg_font_size,
                                    "color": None,
                                    "name": spans[0]["font"] if spans else "Helvetica",
                                },
                            }],
                        })
                        para_index += 1
        
        # Don't forget the last section
        if current["paragraphs"]:
            sections.append(current)
        
        doc.close()
        
        logger.info(f"Extracted {len(sections)} sections from PDF ({para_index} paragraphs)")
        
        return {"sections": sections}
    
    except Exception as e:
        logger.error(f"Error extracting PDF: {e}", exc_info=True)
        raise
