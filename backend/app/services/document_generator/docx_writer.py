"""
Production-grade DOCX template preservation.

Writes enhanced text back into the ORIGINAL docx's existing paragraph
runs while preserving ALL formatting. Handles multi-run paragraphs
intelligently to maintain inline formatting where possible.

This is the core USP of the product - true template preservation.
"""
import logging
from docx import Document
from docx.shared import RGBColor, Pt
from typing import List, Dict

logger = logging.getLogger(__name__)


def _preserve_run_formatting(run, new_text: str):
    """Apply text to run while preserving all formatting"""
    run.text = new_text
    # All formatting (bold, italic, font, size, color) is preserved
    # because we're modifying the existing run, not creating a new one


def _split_text_intelligently(text: str, num_runs: int) -> List[str]:
    """
    Split text into parts that respect word boundaries.
    Tries to distribute text roughly evenly across runs.
    """
    if num_runs <= 1:
        return [text]
    
    words = text.split()
    if len(words) <= num_runs:
        # Not enough words to split meaningfully
        return [text]
    
    # Calculate words per run
    words_per_run = len(words) // num_runs
    
    parts = []
    current_idx = 0
    
    for i in range(num_runs - 1):
        end_idx = current_idx + words_per_run
        part = " ".join(words[current_idx:end_idx])
        parts.append(part)
        current_idx = end_idx
    
    # Last run gets remaining words
    parts.append(" ".join(words[current_idx:]))
    
    return parts


def apply_changes(source_path: str, output_path: str, changes: List[dict]) -> int:
    """
    Apply changes to DOCX while preserving maximum formatting.
    
    Strategy:
    1. For single-run paragraphs: Simple replacement (perfect preservation)
    2. For multi-run paragraphs: Try to intelligently distribute text across runs
       to preserve inline formatting where possible
    
    Returns:
        Number of paragraphs successfully modified
    """
    try:
        logger.info(f"Applying changes to DOCX: {source_path} -> {output_path}")
        
        doc = Document(source_path)
        by_index = {c["para_index"]: c["after"] for c in changes}
        
        applied = 0
        
        for p_index, para in enumerate(doc.paragraphs):
            if p_index in by_index:
                new_text = by_index[p_index]
                
                if not para.runs:
                    logger.warning(f"Paragraph {p_index} has no runs, skipping")
                    continue
                
                # Strategy 1: Single run - perfect preservation
                if len(para.runs) == 1:
                    _preserve_run_formatting(para.runs[0], new_text)
                    applied += 1
                    logger.debug(f"Applied change to single-run paragraph {p_index}")
                
                # Strategy 2: Multiple runs - intelligent distribution
                elif len(para.runs) > 1:
                    # Check if we can split the text meaningfully
                    if ' ' in new_text and len(new_text.split()) >= len(para.runs):
                        # Split text across runs proportionally
                        text_parts = _split_text_intelligently(new_text, len(para.runs))
                        
                        for i, run in enumerate(para.runs):
                            if i < len(text_parts):
                                _preserve_run_formatting(run, text_parts[i])
                            else:
                                _preserve_run_formatting(run, "")
                        
                        logger.debug(f"Applied change to multi-run paragraph {p_index} with split")
                    else:
                        # Text too short to split, use first run and clear others
                        _preserve_run_formatting(para.runs[0], new_text)
                        for run in para.runs[1:]:
                            _preserve_run_formatting(run, "")
                        
                        logger.debug(f"Applied change to multi-run paragraph {p_index} (collapsed)")
                    
                    applied += 1
        
        # Save with all formatting preserved
        doc.save(output_path)
        logger.info(f"Successfully applied {applied} changes to DOCX")
        
        return applied
    
    except Exception as e:
        logger.error(f"Error applying changes to DOCX: {e}", exc_info=True)
        raise


def validate_docx_integrity(docx_path: str) -> Dict[str, any]:
    """
    Validate that a DOCX file is properly formatted and readable.
    Useful for debugging and quality assurance.
    
    Returns:
        Dictionary with validation results
    """
    try:
        doc = Document(docx_path)
        
        return {
            "valid": True,
            "num_paragraphs": len(doc.paragraphs),
            "num_sections": len(doc.sections),
            "has_tables": len(doc.tables) > 0,
            "has_images": any(
                rel.target_part for rel in doc.part.rels.values() 
                if "image" in rel.target_ref
            ) if hasattr(doc.part, 'rels') else False,
        }
    
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }
