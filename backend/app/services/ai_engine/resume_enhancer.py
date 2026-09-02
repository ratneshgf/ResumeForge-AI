"""
Production-grade Resume Enhancement Engine

Uses real AI to intelligently rewrite resume sections while:
- Preserving factual accuracy (no hallucination)
- Targeting the specific job description
- Maintaining professional tone
- Only modifying appropriate sections
- Never changing personal info, dates, company names, education details

Each section is enhanced independently with detailed prompts and validation.
"""
import logging
from pathlib import Path
from typing import Dict, List

from app.services.ai_engine.client import generate_json, AIClientError
from app.services.ai_engine.jd_analyzer import analyze as analyze_jd

logger = logging.getLogger(__name__)

PROMPT_DIR = Path(__file__).parent / "prompts"

# Sections that should NEVER be modified
PROTECTED_SECTIONS = {"preamble", "contact", "contact information", "personal information"}

# Sections that can be enhanced
OBJECTIVE_HEADINGS = {"career objective", "objective", "summary", "professional summary", "profile"}
SKILLS_HEADINGS = {"technical skills", "skills", "core competencies", "expertise"}
EXPERIENCE_HEADINGS = {"experience", "work experience", "professional experience", "employment history"}
PROJECT_HEADINGS = {"projects", "project", "key projects", "academic projects"}
ACHIEVEMENT_HEADINGS = {"achievements", "accomplishments", "honors", "awards"}


def _load_prompt(filename: str) -> str:
    """Load prompt template from file"""
    prompt_path = PROMPT_DIR / filename
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {filename}")
    return prompt_path.read_text()


def _identify_section_type(heading: str) -> str:
    """Identify what type of section this is"""
    heading_lower = heading.strip(":").lower()
    
    if heading_lower in PROTECTED_SECTIONS:
        return "protected"
    elif heading_lower in OBJECTIVE_HEADINGS:
        return "objective"
    elif heading_lower in SKILLS_HEADINGS:
        return "skills"
    elif heading_lower in EXPERIENCE_HEADINGS:
        return "experience"
    elif heading_lower in PROJECT_HEADINGS:
        return "project"
    elif heading_lower in ACHIEVEMENT_HEADINGS:
        return "achievement"
    elif "education" in heading_lower or "academic" in heading_lower:
        return "protected"  # Don't modify education section
    else:
        return "other"


def _enhance_objective_section(original_text: str, job_requirements: Dict, job_description: str) -> Dict:
    """
    Enhance career objective/summary section.
    Should be concise, targeted, and highlight relevant skills.
    """
    try:
        prompt_template = _load_prompt("enhance_objective_v2.txt")
        
        prompt = prompt_template.format(
            original_text=original_text,
            job_title=job_requirements.get("job_title", "target role"),
            required_skills=", ".join(job_requirements.get("required_skills", [])[:5]),
            job_description_snippet=job_description[:500]
        )
        
        result = generate_json(prompt, required_keys=["rewritten_text", "changes_made"])
        
        return {
            "rewritten_text": result["rewritten_text"],
            "changes_made": result.get("changes_made", []),
            "confidence": "high"
        }
    
    except AIClientError as e:
        logger.error(f"AI error enhancing objective: {e}")
        raise
    except Exception as e:
        logger.error(f"Error enhancing objective: {e}", exc_info=True)
        raise


def _enhance_skills_section(original_text: str, job_requirements: Dict) -> Dict:
    """
    Enhance skills section by:
    - Adding relevant missing skills that can be inferred from experience
    - Reorganizing to prioritize JD-relevant skills
    - Never inventing skills with no evidence
    """
    try:
        prompt_template = _load_prompt("enhance_skills_v2.txt")
        
        required_skills = job_requirements.get("required_skills", [])
        preferred_skills = job_requirements.get("preferred_skills", [])
        
        prompt = prompt_template.format(
            original_text=original_text,
            required_skills=", ".join(required_skills),
            preferred_skills=", ".join(preferred_skills[:10])
        )
        
        result = generate_json(prompt, required_keys=["rewritten_text", "added_skills"])
        
        return {
            "rewritten_text": result["rewritten_text"],
            "added_skills": result.get("added_skills", []),
            "confidence": "high"
        }
    
    except AIClientError as e:
        logger.error(f"AI error enhancing skills: {e}")
        raise
    except Exception as e:
        logger.error(f"Error enhancing skills: {e}", exc_info=True)
        raise


def _enhance_experience_bullet(original_text: str, job_requirements: Dict) -> Dict:
    """
    Enhance experience/project bullet points by:
    - Using stronger action verbs
    - Quantifying results where possible
    - Highlighting relevant technologies
    - Aligning with job requirements
    - Never changing facts, dates, or company names
    """
    try:
        prompt_template = _load_prompt("enhance_bullet_v2.txt")
        
        prompt = prompt_template.format(
            original_text=original_text,
            required_skills=", ".join(job_requirements.get("required_skills", [])[:10]),
            keywords=", ".join(job_requirements.get("keywords", [])[:15])
        )
        
        result = generate_json(prompt, required_keys=["rewritten_text", "improvements"])
        
        return {
            "rewritten_text": result["rewritten_text"],
            "improvements": result.get("improvements", []),
            "confidence": "medium"
        }
    
    except AIClientError as e:
        logger.error(f"AI error enhancing bullet: {e}")
        raise
    except Exception as e:
        logger.error(f"Error enhancing bullet: {e}", exc_info=True)
        raise


def enhance_section(section_heading: str, original_text: str, job_description: str, 
                    full_resume_context: str = "") -> Dict:
    """
    Enhance a single resume section based on its type.
    
    Returns:
        dict with keys: rewritten_text, changes_made, confidence, section_type
    """
    section_type = _identify_section_type(section_heading)
    
    # Don't modify protected sections
    if section_type == "protected":
        logger.info(f"Skipping protected section: {section_heading}")
        return {
            "rewritten_text": original_text,
            "changes_made": [],
            "confidence": "n/a",
            "section_type": section_type,
            "modified": False
        }
    
    # Don't modify very short text (likely labels or headers)
    if len(original_text.strip()) < 10:
        return {
            "rewritten_text": original_text,
            "changes_made": [],
            "confidence": "n/a",
            "section_type": section_type,
            "modified": False
        }
    
    try:
        # Analyze job description once
        job_requirements = analyze_jd(job_description)
        
        # Route to appropriate enhancement function
        if section_type == "objective":
            result = _enhance_objective_section(original_text, job_requirements, job_description)
        elif section_type == "skills":
            result = _enhance_skills_section(original_text, job_requirements)
        elif section_type in ["experience", "project", "achievement"]:
            result = _enhance_experience_bullet(original_text, job_requirements)
        else:
            # For unknown section types, attempt generic enhancement
            result = _enhance_experience_bullet(original_text, job_requirements)
        
        result["section_type"] = section_type
        result["modified"] = result["rewritten_text"] != original_text
        
        return result
    
    except AIClientError as e:
        # Propagate AI errors up so user knows AI failed
        logger.error(f"AI error in enhance_section: {e}")
        raise
    
    except Exception as e:
        logger.error(f"Error in enhance_section: {e}", exc_info=True)
        # Return original on unexpected errors
        return {
            "rewritten_text": original_text,
            "changes_made": [],
            "confidence": "error",
            "section_type": section_type,
            "modified": False,
            "error": str(e)
        }


def enhance_resume(sections: List[dict], job_description: str) -> List[dict]:
    """
    Enhance entire resume by processing each section.
    
    Returns list of changes with detailed information about what was modified.
    """
    changes = []
    full_resume_text = _flatten_resume_text(sections)
    
    logger.info(f"Starting resume enhancement for {len(sections)} sections")
    
    for section in sections:
        heading = section["heading"]
        section_type = _identify_section_type(heading)
        
        # Skip protected sections entirely
        if section_type == "protected":
            logger.info(f"Skipping protected section: {heading}")
            continue
        
        # Process each paragraph in the section
        for para in section["paragraphs"]:
            para_text = para["text"].strip()
            
            # Skip very short paragraphs
            if len(para_text) < 10:
                logger.info(f"Skipping short paragraph ({len(para_text)} chars): {para_text[:50]}")
                continue
                
            try:
                logger.info(f"Enhancing paragraph in {heading}: {para_text[:100]}...")
                
                result = enhance_section(
                    heading, 
                    para_text, 
                    job_description,
                    full_resume_text
                )
                
                rewritten = result["rewritten_text"].strip()
                original = para_text
                
                logger.info(f"AI returned text ({len(rewritten)} chars): {rewritten[:100]}...")
                logger.info(f"Original vs Rewritten match: {original == rewritten}")
                
                # Compare normalized versions (strip whitespace, case insensitive for comparison)
                normalized_original = " ".join(original.lower().split())
                normalized_rewritten = " ".join(rewritten.lower().split())
                
                # Only add to changes if text was actually modified
                if normalized_original != normalized_rewritten:
                    changes.append({
                        "para_index": para["para_index"],
                        "heading": heading,
                        "before": original,
                        "after": rewritten,
                        "section_type": result["section_type"],
                        "changes_made": result.get("changes_made", []),
                        "confidence": result.get("confidence", "medium")
                    })
                    logger.info(f"✓ Enhanced paragraph in {heading} section - changes detected")
                else:
                    logger.warning(f"✗ No changes for paragraph in {heading} - AI returned same text")
            
            except AIClientError as e:
                # Propagate AI errors - user needs to know AI failed
                logger.error(f"AI enhancement failed: {e}")
                raise
            
            except Exception as e:
                logger.error(f"Error enhancing paragraph in {heading}: {e}", exc_info=True)
                # Continue with other paragraphs even if one fails
                continue
    
    logger.info(f"Resume enhancement complete. Generated {len(changes)} changes.")
    
    # If no changes were generated, log a warning
    if len(changes) == 0:
        logger.warning("No changes generated! This might indicate an issue with AI prompts or resume content.")
    
    return changes


def _flatten_resume_text(sections: List[dict]) -> str:
    """Extract full resume text for context"""
    parts = []
    for section in sections:
        parts.append(section["heading"])
        for para in section["paragraphs"]:
            parts.append(para["text"])
    return " ".join(parts)
