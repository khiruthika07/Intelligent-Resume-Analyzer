"""
Intelligent Resume Analyzer - Resume Parser
Parses text resumes to extract candidate details: Name, Email, Phone, Skills, Education, Experience, Keywords.
Uses ONLY Python Standard Library.
"""

import os
import re
from typing import Dict, List, Any, Optional
from utils import extract_skills_from_text, extract_keywords_from_text, normalize_text


class ResumeParser:
    """Parses candidate resume files (.txt) and extracts structured candidate profiles."""

    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        """Reads a .txt resume file and returns parsed information."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume file not found: {file_path}")

        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        return ResumeParser.parse_text(content, filename=filename)

    @staticmethod
    def parse_text(resume_text: str, filename: str = "Candidate") -> Dict[str, Any]:
        """Parses resume text content into structured dict."""
        if not resume_text or not resume_text.strip():
            fallback_name = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
            return {
                'filename': filename,
                'raw_text': '',
                'name': fallback_name,
                'email': 'N/A',
                'phone': 'N/A',
                'skills': [],
                'education_level': 'None',
                'education_details': 'Not Specified',
                'experience_years': 0.0,
                'experience_details': 'No experience recorded',
                'keywords': []
            }

        # 1. Extract Contact Info
        email = ResumeParser._extract_email(resume_text)
        phone = ResumeParser._extract_phone(resume_text)
        name = ResumeParser._extract_name(resume_text, filename=filename)

        # 2. Extract Skills
        skills = extract_skills_from_text(resume_text)

        # 3. Extract Education
        edu_level, edu_details = ResumeParser._extract_education(resume_text)

        # 4. Extract Experience
        exp_years, exp_details = ResumeParser._extract_experience(resume_text)

        # 5. Extract Keywords
        keywords = extract_keywords_from_text(resume_text, top_n=25)

        return {
            'filename': filename,
            'raw_text': resume_text,
            'name': name,
            'email': email,
            'phone': phone,
            'skills': skills,
            'education_level': edu_level,
            'education_details': edu_details,
            'experience_years': exp_years,
            'experience_details': exp_details,
            'keywords': keywords
        }

    @staticmethod
    def _extract_email(text: str) -> str:
        """Extracts candidate email using regex."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        return match.group(0) if match else "N/A"

    @staticmethod
    def _extract_phone(text: str) -> str:
        """Extracts candidate phone number using regex patterns."""
        phone_patterns = [
            r'(?:\+?\d{1,3}[\s\.-]?)?\(?\d{3}\)?[\s\.-]?\d{3}[\s\.-]?\d{4}',
            r'\+?\d{10,12}\b',
            r'\b\d{5}[\s\-]\d{5}\b'
        ]
        for pat in phone_patterns:
            match = re.search(pat, text)
            if match:
                phone_str = match.group(0).strip()
                # Exclude strings that look like years or small integers
                if len(re.sub(r'\D', '', phone_str)) >= 10:
                    return phone_str
        return "N/A"

    @staticmethod
    def _extract_name(text: str, filename: str = "") -> str:
        """
        Extracts candidate name using text heuristics on top lines,
        excluding headers and common labels.
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        invalid_words = {
            "resume", "curriculum", "vitae", "cv", "profile", "summary",
            "contact", "email", "phone", "address", "education", "experience",
            "skills", "projects", "objective", "page", "developer", "engineer"
        }

        # Check explicit label first e.g. Name: Anjali Kumar
        for line in lines[:8]:
            label_match = re.search(r'^(?:name|candidate name)\s*:\s*(.+)$', line, re.IGNORECASE)
            if label_match:
                candidate_name = label_match.group(1).strip()
                if len(candidate_name) > 2:
                    return candidate_name.title()

        # Check top lines for title case name
        for line in lines[:5]:
            clean_line = re.sub(r'[^a-zA-Z\s]', '', line).strip()
            words = clean_line.split()

            # Typically 2-4 words, starts with uppercase
            if 1 <= len(words) <= 4:
                lower_words = [w.lower() for w in words]
                if not any(w in invalid_words for w in lower_words):
                    if all(len(w) >= 2 for w in words) and any(w[0].isupper() for w in words):
                        return clean_line.title()

        # Fallback to filename
        if filename:
            name_part = os.path.splitext(filename)[0]
            name_part = re.sub(r'^(?:resume|cv)[_\-\s]*', '', name_part, flags=re.IGNORECASE)
            name_part = re.sub(r'[_\-\s]*(?:resume|cv)$', '', name_part, flags=re.IGNORECASE)
            clean_name = name_part.replace('_', ' ').replace('-', ' ').strip().title()
            if clean_name:
                return clean_name

        return "Unknown Candidate"

    @staticmethod
    def _extract_education(text: str) -> tuple:
        """
        Extracts candidate's highest education level and summary detail string.
        Returns (level: str, details: str)
        Level hierarchy: PhD > Master > Bachelor > Diploma > High School > None
        """
        text_lower = text.lower()
        details_list = []

        level = "None"
        if re.search(r'\b(phd|ph\.d|doctorate)\b', text_lower):
            level = "PhD"
        elif re.search(r'\b(master|masters|m\.tech|m\.e|m\.sc|mca|ms|mba)\b', text_lower):
            level = "Master"
        elif re.search(r'\b(bachelor|bachelors|b\.tech|b\.e|b\.sc|bca|bs|b\.com|degree)\b', text_lower):
            level = "Bachelor"
        elif re.search(r'\b(diploma|associate)\b', text_lower):
            level = "Diploma"
        elif re.search(r'\b(high school|secondary|12th|10th)\b', text_lower):
            level = "High School"

        # Search for specific degree names for details
        degree_patterns = [
            r'\b(b\.tech|b\.e|b\.sc|bca|m\.tech|m\.e|m\.sc|mca|ph\.d|diploma)\s*(?:in\s+)?([a-zA-Z\s,]+)?\b',
            r'\b(bachelor|master|doctorate)\s+of\s+([a-zA-Z\s]+)\b'
        ]

        for pat in degree_patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            for m in matches:
                if isinstance(m, tuple):
                    deg_str = " ".join([part for part in m if part]).strip()
                else:
                    deg_str = m.strip()
                if len(deg_str) < 50 and deg_str not in details_list:
                    details_list.append(deg_str.title())

        details_str = ", ".join(details_list[:2]) if details_list else f"{level} Degree"
        return level, details_str

    @staticmethod
    def _extract_experience(text: str) -> tuple:
        """
        Calculates experience in years from explicit statements or employment date ranges.
        Returns (years: float, summary_detail: str)
        """
        # 1. Look for explicit total experience statements e.g. "5 years of experience", "3+ yrs exp"
        explicit_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:\+|-\s*\d+)?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:work\s+)?experience\b',
            r'total\s+experience\s*:\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b',
            r'experience\s*:\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b'
        ]

        explicit_years = []
        for pat in explicit_patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            for m in matches:
                try:
                    val = float(m)
                    if 0 <= val <= 35:
                        explicit_years.append(val)
                except ValueError:
                    continue

        if explicit_years:
            tot_exp = max(explicit_years)
            return tot_exp, f"{tot_exp:.1f} years total experience"

        # 2. Date ranges scanning e.g. "2020 - 2023", "2019 - Present", "Jan 2021 to Mar 2023"
        date_pattern = r'\b(20\d{2}|19\d{2})\s*(?:-|to|–)\s*(20\d{2}|19\d{2}|present|current|now)\b'
        date_matches = re.findall(date_pattern, text, re.IGNORECASE)

        total_months = 0
        current_year = 2026

        for start_str, end_str in date_matches:
            try:
                start_yr = int(start_str)
                if end_str.lower() in ['present', 'current', 'now']:
                    end_yr = current_year
                else:
                    end_yr = int(end_str)

                diff = max(0, end_yr - start_yr)
                # Ignore degree dates (like 4-year college 2018-2022) if it overlaps with education keywords
                total_months += diff * 12
            except ValueError:
                continue

        # Convert months to years (capped or adjusted)
        calculated_years = round(total_months / 12.0, 1)

        # Avoid misinterpreting 4 years of college as 4 years of experience if no explicit work experience header exists
        has_work_header = bool(re.search(r'\b(work experience|employment|professional experience|career)\b', text, re.IGNORECASE))
        if not has_work_header and calculated_years > 0:
            calculated_years = round(calculated_years * 0.5, 1)  # Discount non-explicit work dates

        summary = f"{calculated_years:.1f} years experience" if calculated_years > 0 else "Fresh Graduate / Entry Level"
        return calculated_years, summary
