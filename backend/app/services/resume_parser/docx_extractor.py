"""
Production-grade DOCX extraction with enhanced section detection.

Extracts a normalized schema from .docx resumes with intelligent section
recognition, preserving all formatting details for template preservation.
"""
import logging
from docx import Document
from typing import List, Dict

logger = logging.getLogger(__name__)

# Comprehensive section keyword mapping
SECTION_KEYWORDS = {
    "contact": ["contact", "contact information", "personal information", "reach me"],
    "objective": ["career objective", "objective", "summary", "professional summary", 
                  "profile", "about me", "career summary"],
    "experience": ["experience", "work experience", "professional experience", 
                   "employment history", "work history", "career history"],
    "education": ["education", "academic background", "qualifications", "academic qualifications",
                  "educational background"],
    "skills": ["technical skills", "skills", "core competencies", "expertise", 
               "technical proficiencies", "key skills", "professional skills"],
    "projects": ["projects", "key projects", "academic projects", "personal projects", 
                 "portfolio", "project work"],
    "certifications": ["certifications", "certificates", "professional certifications",
                      "licenses", "accreditations"],
    "achievements": ["achievements", "accomplishments", "honors", "awards", "recognition"],
    "publications": ["publications", "research", "papers", "articles"],
    "interests": ["interests", "hobbies", "personal interests"],
}

BODY_FONT_SIZE = 11  # baseline for body text


def _normalize_heading(heading: str) -> str:
    """Normalize heading to standard format"""
    heading_lower = heading.strip(":").strip().lower()
    
    # Map to standard categories
    for category, keywords in SECTION_KEYWORDS.items():
        if any(keyword == heading_lower or keyword in heading_lower for keyword in keywords):
            return category.upper()
    
    # Return original if no match
    return heading.strip()


def _run_style(run) -> dict:
    """Extract complete style information from a run"""
    style = {
        "bold": bool(run.bold),
        "italic": bool(run.italic),
        "underline": bool(run.underline),
        "size_pt": run.font.size.pt if run.font.size else None,
        "color": str(run.font.color.rgb) if run.font.color and hasattr(run.font.color, 'rgb') and run.font.color.rgb else None,
        "name": run.font.name,
    }
    
    return style


def _is_heading(para, text: str) -> bool:
    """
    Determine if a paragraph is a section heading using multiple heuristics:
    1. Font size larger than body
    2. Bold formatting
    3. Matches known section keywords
    4. All caps
    5. Short length (< 50 chars)
    """
    if not para.runs:
        return False
    
    text_lower = text.strip(":").lower()
    
    # Check for section keywords (strong signal)
    for keywords in SECTION_KEYWORDS.values():
        if any(keyword == text_lower or keyword in text_lower for keyword in keywords):
            return True
    
    # Analyze formatting
    font_sizes = [r.font.size.pt if r.font.size else 0 for r in para.runs]
    max_size = max(font_sizes) if font_sizes else 0
    any_bold = any(r.bold for r in para.runs)
    
    # Heading if: bold AND (larger font OR matches keyword pattern)
    if any_bold and max_size and max_size > BODY_FONT_SIZE:
        return True
    
    # All caps and short could be a heading
    if text.isupper() and len(text) < 50 and any_bold:
        return True
    
    return False


def extract(path: str) -> dict:
    """
    Extract structured data from DOCX with intelligent section detection.
    
    Returns:
        Dictionary with 'sections' key containing list of section dicts
    """
    try:
        logger.info(f"Extracting DOCX: {path}")
        
        doc = Document(path)
        sections: List[dict] = []
        current = {"heading": "PREAMBLE", "paragraphs": []}
        
        for p_index, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            
            if not text:
                continue
            
            # Extract run information with styles
            runs = [
                {
                    "run_index": r_i,
                    "text": r.text,
                    "style": _run_style(r)
                }
                for r_i, r in enumerate(para.runs)
            ]
            
            # Determine if this is a heading
            is_heading = _is_heading(para, text)
            
            if is_heading:
                # Save previous section if it has content
                if current["paragraphs"]:
                    sections.append(current)
                
                # Start new section with normalized heading
                normalized_heading = _normalize_heading(text)
                current = {"heading": normalized_heading, "paragraphs": []}
                logger.debug(f"Detected section heading: {text} -> {normalized_heading}")
            else:
                # Add as paragraph to current section
                current["paragraphs"].append({
                    "para_index": p_index,
                    "style_name": para.style.name,
                    "text": text,
                    "runs": runs,
                })
        
        # Don't forget the last section
        if current["paragraphs"]:
            sections.append(current)
        
        logger.info(f"Extracted {len(sections)} sections from DOCX")
        
        return {"sections": sections}
    
    except Exception as e:
        logger.error(f"Error extracting DOCX: {e}", exc_info=True)
        raise
