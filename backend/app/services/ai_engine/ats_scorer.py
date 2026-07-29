"""
Production-grade ATS Scoring Engine

Uses multiple NLP techniques to provide accurate, realistic ATS scores:
- Semantic similarity (Sentence Transformers)
- Keyword matching (TF-IDF, Cosine Similarity)
- Skill extraction and matching (spaCy NER + comprehensive taxonomy)
- Experience relevance scoring
- Education matching
- Resume completeness checks
- Formatting compatibility analysis

Each component is weighted and explained to provide actionable feedback.
"""
import logging
import re
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import settings
from app.services.ai_engine.skill_taxonomy import SkillTaxonomy

# Initialize NLP models (lazy loading)
_nlp_model = None
_sentence_model = None
_stop_words = None
_skill_taxonomy = None

logger = logging.getLogger(__name__)


def _get_nlp_model():
    """Lazy load spaCy model"""
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load(settings.SPACY_MODEL)
        except OSError:
            logger.warning(f"spaCy model {settings.SPACY_MODEL} not found, downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", settings.SPACY_MODEL])
            _nlp_model = spacy.load(settings.SPACY_MODEL)
    return _nlp_model


def _get_sentence_model():
    """Lazy load Sentence Transformer model"""
    global _sentence_model
    if _sentence_model is None:
        _sentence_model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
    return _sentence_model


def _get_stop_words():
    """Lazy load NLTK stopwords"""
    global _stop_words
    if _stop_words is None:
        try:
            _stop_words = set(stopwords.words('english'))
        except LookupError:
            import nltk
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt', quiet=True)
            _stop_words = set(stopwords.words('english'))
    return _stop_words


def _get_skill_taxonomy():
    """Lazy load skill taxonomy"""
    global _skill_taxonomy
    if _skill_taxonomy is None:
        _skill_taxonomy = SkillTaxonomy()
    return _skill_taxonomy


def _flatten_resume_text(sections: List[dict]) -> str:
    """Extract all text from resume sections"""
    parts = []
    for section in sections:
        parts.append(section["heading"])
        for para in section["paragraphs"]:
            parts.append(para["text"])
    return " ".join(parts)


def _extract_section_text(sections: List[dict], section_names: List[str]) -> str:
    """Extract text from specific sections"""
    text_parts = []
    for section in sections:
        heading_lower = section["heading"].lower()
        if any(name in heading_lower for name in section_names):
            for para in section["paragraphs"]:
                text_parts.append(para["text"])
    return " ".join(text_parts)


def _extract_keywords(text: str, top_n: int = 20) -> List[Tuple[str, float]]:
    """Extract top keywords using TF-IDF"""
    stop_words = _get_stop_words()
    
    # Tokenize and clean
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalnum() and t not in stop_words and len(t) > 2]
    
    if not tokens:
        return []
    
    # Use TF-IDF
    vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([" ".join(tokens)])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        keywords = [(feature_names[i], float(scores[i])) 
                    for i in np.argsort(scores)[::-1] if scores[i] > 0]
        return keywords[:top_n]
    except:
        # Fallback to simple frequency
        counter = Counter(tokens)
        return [(word, count / len(tokens)) for word, count in counter.most_common(top_n)]


def _compute_semantic_similarity(text1: str, text2: str) -> float:
    """Compute semantic similarity using sentence transformers"""
    try:
        model = _get_sentence_model()
        embeddings = model.encode([text1, text2])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(similarity)
    except Exception as e:
        logger.error(f"Error computing semantic similarity: {e}")
        return 0.0


def _extract_years_of_experience(text: str) -> int:
    """Extract years of experience from text"""
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
        r'(?:experience|exp).*?(\d+)\+?\s*(?:years?|yrs?)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            return max([int(m) for m in matches])
    
    return 0


def _extract_education_level(text: str) -> str:
    """Extract highest education level"""
    text_lower = text.lower()
    
    if any(term in text_lower for term in ['phd', 'ph.d', 'doctorate']):
        return 'PhD'
    elif any(term in text_lower for term in ['master', 'ms', 'm.s', 'mba', 'mtech', 'm.tech']):
        return 'Masters'
    elif any(term in text_lower for term in ['bachelor', 'bs', 'b.s', 'be', 'b.e', 'btech', 'b.tech', 'ba', 'b.a']):
        return 'Bachelors'
    elif any(term in text_lower for term in ['associate', 'diploma']):
        return 'Associate'
    
    return 'Unknown'


def _check_resume_completeness(sections: List[dict]) -> Dict[str, bool]:
    """Check if resume has all essential sections"""
    section_headings = [s["heading"].lower() for s in sections]
    
    has_contact = any('contact' in h or 'email' in h or 'phone' in h or h == 'preamble' 
                      for h in section_headings)
    has_experience = any('experience' in h or 'work' in h or 'employment' in h 
                         for h in section_headings)
    has_education = any('education' in h or 'academic' in h or 'qualification' in h 
                        for h in section_headings)
    has_skills = any('skill' in h or 'technical' in h or 'competenc' in h 
                     for h in section_headings)
    has_summary = any('summary' in h or 'objective' in h or 'profile' in h 
                      for h in section_headings)
    
    return {
        'has_contact': has_contact,
        'has_experience': has_experience,
        'has_education': has_education,
        'has_skills': has_skills,
        'has_summary': has_summary,
    }


def score(sections: List[dict], job_description: str) -> dict:
    """
    Comprehensive ATS scoring using multiple NLP techniques
    
    Returns detailed scoring breakdown with explanations
    """
    try:
        resume_text = _flatten_resume_text(sections)
        resume_text_lower = resume_text.lower()
        jd_lower = job_description.lower()
        
        # Initialize skill taxonomy
        skill_taxonomy = _get_skill_taxonomy()
        
        # 1. SKILL MATCHING (25% weight)
        logger.info("Extracting skills from JD and resume")
        jd_skills = skill_taxonomy.extract_skills(job_description)
        resume_skills = skill_taxonomy.extract_skills(resume_text)
        
        matched_skills = [s for s in jd_skills if s in resume_skills]
        missing_skills = [s for s in jd_skills if s not in resume_skills]
        
        skill_match_score = (len(matched_skills) / len(jd_skills) * 100) if jd_skills else 100
        
        # 2. KEYWORD MATCHING (20% weight)
        logger.info("Extracting and matching keywords")
        jd_keywords = _extract_keywords(job_description, top_n=30)
        jd_keyword_terms = [kw[0] for kw in jd_keywords]
        
        matched_keywords = []
        missing_keywords = []
        
        for keyword, score in jd_keywords:
            if keyword in resume_text_lower:
                matched_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        keyword_match_score = (len(matched_keywords) / len(jd_keyword_terms) * 100) if jd_keyword_terms else 100
        
        # 3. SEMANTIC SIMILARITY (25% weight)
        logger.info("Computing semantic similarity")
        semantic_score = _compute_semantic_similarity(resume_text[:2000], job_description[:2000]) * 100
        
        # 4. EXPERIENCE MATCHING (15% weight)
        jd_years_required = _extract_years_of_experience(job_description)
        resume_years = _extract_years_of_experience(resume_text)
        
        if jd_years_required > 0:
            experience_score = min(100, (resume_years / jd_years_required) * 100)
        else:
            experience_score = 100 if resume_years > 0 else 50
        
        # 5. EDUCATION MATCHING (10% weight)
        jd_education = _extract_education_level(job_description)
        resume_education = _extract_education_level(resume_text)
        
        education_levels = {'PhD': 4, 'Masters': 3, 'Bachelors': 2, 'Associate': 1, 'Unknown': 0}
        jd_level = education_levels.get(jd_education, 0)
        resume_level = education_levels.get(resume_education, 0)
        
        if jd_level > 0:
            education_score = min(100, (resume_level / jd_level) * 100)
        else:
            education_score = 100 if resume_level > 0 else 50
        
        # 6. RESUME COMPLETENESS (5% weight)
        completeness = _check_resume_completeness(sections)
        completeness_score = (sum(completeness.values()) / len(completeness)) * 100
        
        # Calculate weighted overall score
        overall_score = round(
            skill_match_score * 0.25 +
            keyword_match_score * 0.20 +
            semantic_score * 0.25 +
            experience_score * 0.15 +
            education_score * 0.10 +
            completeness_score * 0.05
        )
        
        # Generate actionable suggestions
        suggestions = []
        
        if skill_match_score < 70:
            suggestions.append(f"Add {min(3, len(missing_skills))} critical skills: {', '.join(missing_skills[:3])}")
        
        if keyword_match_score < 70:
            suggestions.append(f"Include key terms: {', '.join(missing_keywords[:3])}")
        
        if semantic_score < 60:
            suggestions.append("Align your experience descriptions more closely with the job requirements")
        
        if experience_score < 80 and jd_years_required > 0:
            suggestions.append(f"Highlight {jd_years_required}+ years of relevant experience more prominently")
        
        if not completeness['has_summary']:
            suggestions.append("Add a professional summary targeting this role")
        
        if len(matched_skills) < 5:
            suggestions.append("Demonstrate more technical skills through project descriptions")
        
        # Missing critical sections
        if not completeness['has_experience']:
            suggestions.append("Add work experience section with relevant roles")
        
        if not completeness['has_education']:
            suggestions.append("Include education section with degrees and certifications")
        
        return {
            "score": max(0, min(100, overall_score)),  # Clamp between 0-100
            "breakdown": {
                "skill_match": round(skill_match_score),
                "keyword_match": round(keyword_match_score),
                "semantic_similarity": round(semantic_score),
                "experience_match": round(experience_score),
                "education_match": round(education_score),
                "completeness": round(completeness_score),
            },
            "skills_match_pct": round(skill_match_score),
            "keyword_match_pct": round(keyword_match_score),
            "matched_skills": matched_skills[:20],  # Top 20
            "missing_skills": missing_skills[:10],  # Top 10
            "matched_keywords": matched_keywords[:15],
            "missing_keywords": missing_keywords[:10],
            "suggestions": suggestions[:5],  # Top 5 actionable items
            "completeness_check": completeness,
            "experience_years": {
                "required": jd_years_required,
                "found": resume_years,
            },
            "education": {
                "required": jd_education,
                "found": resume_education,
            }
        }
    
    except Exception as e:
        logger.error(f"Error in ATS scoring: {e}", exc_info=True)
        # Return a safe fallback but log the error
        return {
            "score": 0,
            "breakdown": {
                "skill_match": 0,
                "keyword_match": 0,
                "semantic_similarity": 0,
                "experience_match": 0,
                "education_match": 0,
                "completeness": 0,
            },
            "skills_match_pct": 0,
            "keyword_match_pct": 0,
            "matched_skills": [],
            "missing_skills": [],
            "matched_keywords": [],
            "missing_keywords": [],
            "suggestions": ["Error analyzing resume. Please try again."],
            "completeness_check": {},
            "experience_years": {"required": 0, "found": 0},
            "education": {"required": "Unknown", "found": "Unknown"},
            "error": str(e)
        }
