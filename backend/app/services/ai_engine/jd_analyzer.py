"""
Production-grade Job Description Analyzer

Uses AI and NLP to extract comprehensive information from job descriptions:
- Required and preferred skills
- Experience requirements
- Education requirements
- Key responsibilities
- Important keywords for ATS optimization

Falls back to skill taxonomy extraction if AI fails.
"""
import logging
import re
from pathlib import Path
from typing import Dict

from app.services.ai_engine.client import generate_json, AIClientError
from app.services.ai_engine.skill_taxonomy import SkillTaxonomy

logger = logging.getLogger(__name__)

PROMPT_PATH = Path(__file__).parent / "prompts" / "jd_analysis_v2.txt"

_skill_taxonomy = None


def _get_skill_taxonomy():
    """Lazy load skill taxonomy"""
    global _skill_taxonomy
    if _skill_taxonomy is None:
        _skill_taxonomy = SkillTaxonomy()
    return _skill_taxonomy


def _extract_with_skill_taxonomy(job_description: str) -> Dict:
    """
    Fallback extraction using skill taxonomy when AI fails.
    More sophisticated than the old hardcoded list.
    """
    logger.info("Using skill taxonomy fallback for JD analysis")
    
    skill_taxonomy = _get_skill_taxonomy()
    all_skills = skill_taxonomy.extract_skills(job_description)
    
    text_lower = job_description.lower()
    
    # Split into required vs preferred based on section headers
    required_section_match = re.search(
        r'(?:required|must have|qualifications|requirements)(.*?)(?:preferred|nice to have|bonus|$)',
        text_lower,
        re.DOTALL
    )
    
    if required_section_match:
        required_text = required_section_match.group(1)
        required_skills = [s for s in all_skills if s.lower() in required_text]
        preferred_skills = [s for s in all_skills if s not in required_skills]
    else:
        # If can't split, assume first 70% are required, rest preferred
        split_point = int(len(all_skills) * 0.7)
        required_skills = all_skills[:split_point]
        preferred_skills = all_skills[split_point:]
    
    # Extract years of experience
    years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)'
    years_matches = re.findall(years_pattern, text_lower)
    years_required = max([int(y) for y in years_matches]) if years_matches else 0
    
    # Extract job title
    title_patterns = [
        r'(?:position|role|job):\s*([^\n]+)',
        r'(?:hiring|seeking|looking for)(?:\s+a(?:n)?)?\s+([^\n]+)',
    ]
    job_title = "Software Engineer"  # Default
    for pattern in title_patterns:
        match = re.search(pattern, text_lower)
        if match:
            job_title = match.group(1).strip()
            break
    
    return {
        "job_title": job_title,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "keywords": all_skills[:30],  # Top 30 skills as keywords
        "years_of_experience": years_required,
        "education_required": _extract_education(text_lower),
        "key_responsibilities": _extract_responsibilities(job_description),
    }


def _extract_education(text: str) -> str:
    """Extract education requirements"""
    if any(term in text for term in ['phd', 'ph.d', 'doctorate']):
        return 'PhD'
    elif any(term in text for term in ['master', 'ms', 'm.s', 'mba']):
        return 'Masters'
    elif any(term in text for term in ['bachelor', 'bs', 'b.s', 'be', 'b.e', 'btech']):
        return 'Bachelors'
    return 'Not specified'


def _extract_responsibilities(text: str) -> list:
    """Extract key responsibilities from JD"""
    # Look for responsibility section
    resp_match = re.search(
        r'(?:responsibilities|duties|you will)(.*?)(?:requirements|qualifications|skills|$)',
        text.lower(),
        re.DOTALL
    )
    
    if not resp_match:
        return []
    
    resp_text = resp_match.group(1)
    
    # Split by bullet points or newlines
    lines = [line.strip() for line in resp_text.split('\n') if line.strip()]
    responsibilities = []
    
    for line in lines:
        # Remove bullet points
        line = re.sub(r'^[\-\*\•]\s*', '', line)
        if len(line) > 20 and len(line) < 200:  # Reasonable length
            responsibilities.append(line)
    
    return responsibilities[:5]  # Top 5


def analyze(job_description: str) -> Dict:
    """
    Analyze job description using AI with fallback to skill taxonomy.
    
    Returns comprehensive analysis including skills, requirements, and keywords.
    """
    try:
        logger.info("Analyzing job description with AI")
        
        # Load prompt template
        prompt_template = PROMPT_PATH.read_text()
        prompt = prompt_template.format(job_description=job_description)
        
        # Call AI with required keys
        required_keys = [
            "job_title",
            "required_skills",
            "preferred_skills",
            "keywords",
            "years_of_experience",
            "education_required",
            "key_responsibilities"
        ]
        
        result = generate_json(prompt, required_keys=required_keys)
        
        logger.info(f"AI analysis successful: found {len(result['required_skills'])} required skills")
        return result
    
    except AIClientError as e:
        logger.warning(f"AI analysis failed: {e}. Using skill taxonomy fallback.")
        return _extract_with_skill_taxonomy(job_description)
    
    except Exception as e:
        logger.error(f"Error in JD analysis: {e}", exc_info=True)
        # Fallback to skill taxonomy
        return _extract_with_skill_taxonomy(job_description)
