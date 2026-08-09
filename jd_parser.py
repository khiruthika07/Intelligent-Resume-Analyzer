"""
Intelligent Resume Analyzer - Job Description Parser
Parses text job descriptions to extract required skills, experience, education, and keywords.
Uses ONLY Python Standard Library.
"""

import re
from typing import Dict, List, Any
from utils import extract_skills_from_text, extract_keywords_from_text, normalize_text


class JDParser:
    """Parses Job Description content to extract key requirements."""

    @staticmethod
    def parse_text(jd_text: str) -> Dict[str, Any]:
        """
        Parses JD text and returns a dictionary of extracted requirements:
        {
            'raw_text': str,
            'title': str,
            'required_skills': List[str],
            'required_experience_years': float,
            'required_education': str,
            'keywords': List[str]
        }
        """
        if not jd_text or not jd_text.strip():
            return {
                'raw_text': '',
                'title': 'Job Description',
                'required_skills': [],
                'required_experience_years': 0.0,
                'required_education': 'Any',
                'keywords': []
            }

        # 1. Title Extraction
        title = JDParser._extract_title(jd_text)

        # 2. Extract Required Skills (Prioritize 'Required Skills:' section if present)
        skills = JDParser._extract_required_skills(jd_text)

        # 3. Extract Experience Requirement (in Years)
        experience_years = JDParser._extract_experience(jd_text)

        # 4. Extract Education Requirement
        education = JDParser._extract_education(jd_text)

        # 5. Extract Keywords
        keywords = extract_keywords_from_text(jd_text, top_n=25)

        return {
            'raw_text': jd_text,
            'title': title,
            'required_skills': skills,
            'required_experience_years': experience_years,
            'required_education': education,
            'keywords': keywords
        }

    @staticmethod
    def _extract_title(text: str) -> str:
        """Extracts job title from top lines of text."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return "Job Description"

        for line in lines[:5]:
            match = re.search(r'(?:role|title|position|job\s+title)\s*:\s*(.+)', line, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        first_line = lines[0]
        if len(first_line) <= 60 and not first_line.lower().startswith(("job description", "overview", "about")):
            return first_line.strip()

        return "Job Description"

    @staticmethod
    def _extract_required_skills(text: str) -> List[str]:
        """Extracts required skills from JD, prioritizing explicit 'Required Skills' sections."""
        # Check if 'Required Skills:' or 'Key Skills:' section exists
        sec_pattern = r'(?:required|key|technical)\s+skills\s*:\s*(.*?)(?=\n\s*(?:experience|education|responsibilities|qualification|role|overview|requirements)\b|$)'
        match = re.search(sec_pattern, text, re.IGNORECASE | re.DOTALL)

        if match:
            skills_section_text = match.group(1)
            section_skills = extract_skills_from_text(skills_section_text)
            if section_skills:
                return section_skills

        # Fallback to full text skill extraction
        return extract_skills_from_text(text)

    @staticmethod
    def _extract_experience(text: str) -> float:
        """Extracts minimum required experience in years using regex patterns."""
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:\+|-\s*\d+)?\s*(?:to\s*\d+)?\s*(?:years?|yrs?)\b',
            r'(?:minimum|at least|req(?:uire[ds]?)?)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b',
            r'(\d+(?:\.\d+)?)\s*\(?\+\)?\s*(?:years?|yrs?)\s+(?:of\s+)?experience\b'
        ]

        exp_values = []
        for pat in patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            for m in matches:
                try:
                    val = float(m)
                    if 0 <= val <= 30:
                        exp_values.append(val)
                except ValueError:
                    continue

        if exp_values:
            return min(exp_values)
        return 0.0

    @staticmethod
    def _extract_education(text: str) -> str:
        """Detects required degree qualification level."""
        text_lower = text.lower()

        if re.search(r'\b(phd|ph\.d|doctorate)\b', text_lower):
            return "PhD"
        if re.search(r'\b(master|masters|m\.tech|m\.e|m\.sc|mca|ms|mba)\b', text_lower):
            return "Master"
        if re.search(r'\b(bachelor|bachelors|b\.tech|b\.e|b\.sc|bca|bs|degree)\b', text_lower):
            return "Bachelor"
        if re.search(r'\b(diploma)\b', text_lower):
            return "Diploma"

        return "Bachelor"
