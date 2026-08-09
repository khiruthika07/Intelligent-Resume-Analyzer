"""
Intelligent Resume Analyzer - Analyzer Controller
Main orchestrator that parses JD and candidate resumes, computes ranked evaluations,
and aggregates dashboard metrics.
Uses ONLY Python Standard Library.
"""

from typing import Dict, List, Any
from jd_parser import JDParser
from resume_parser import ResumeParser
from scorer import Scorer


class ResumeAnalyzer:
    """Orchestrates candidate evaluation pipeline and dynamic dashboard stats."""

    def __init__(self):
        self.jd_profile: Dict[str, Any] = {}
        self.candidate_profiles: List[Dict[str, Any]] = []
        self.evaluations: List[Dict[str, Any]] = []

    def set_job_description(self, jd_text: str) -> Dict[str, Any]:
        """Parses and sets current Job Description."""
        self.jd_profile = JDParser.parse_text(jd_text)
        return self.jd_profile

    def analyze_resumes(self, resume_files: List[str]) -> List[Dict[str, Any]]:
        """
        Parses all given resume files, scores them against set JD,
        ranks them by total score descending, and returns complete evaluation objects.
        """
        if not self.jd_profile:
            raise ValueError("Job Description must be set before analyzing resumes.")

        self.candidate_profiles = []
        self.evaluations = []

        for file_path in resume_files:
            try:
                cand_profile = ResumeParser.parse_file(file_path)
                self.candidate_profiles.append(cand_profile)

                score_info = Scorer.calculate_score(cand_profile, self.jd_profile)

                eval_record = {
                    'candidate_profile': cand_profile,
                    'score_info': score_info,
                    'filename': cand_profile['filename'],
                    'name': cand_profile['name'],
                    'email': cand_profile['email'],
                    'phone': cand_profile['phone'],
                    'skills': cand_profile['skills'],
                    'education_level': cand_profile['education_level'],
                    'education_details': cand_profile['education_details'],
                    'experience_years': cand_profile['experience_years'],
                    'total_score': score_info['total_score'],
                    'recommendation': score_info['recommendation'],
                    'matched_skills': score_info['matched_skills'],
                    'missing_skills': score_info['missing_skills'],
                    'assessment_summary': score_info['assessment_summary']
                }
                self.evaluations.append(eval_record)
            except Exception as e:
                print(f"Error parsing resume {file_path}: {e}")

        # Rank candidates by total_score descending
        self.evaluations.sort(key=lambda x: x['total_score'], reverse=True)

        # Assign rank numbers (1, 2, 3...)
        for idx, item in enumerate(self.evaluations):
            item['rank'] = idx + 1

        return self.evaluations

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Computes aggregate metrics for dashboard stat cards:
        - total_candidates
        - average_score
        - top_candidate
        - highly_suitable_count
        """
        if not self.evaluations:
            return {
                'total_candidates': 0,
                'average_score': 0.0,
                'top_candidate': "N/A",
                'highly_suitable_count': 0
            }

        total_candidates = len(self.evaluations)
        scores = [e['total_score'] for e in self.evaluations]
        avg_score = round(sum(scores) / total_candidates, 1)

        top_candidate = self.evaluations[0]['name'] if self.evaluations else "N/A"
        top_score = self.evaluations[0]['total_score'] if self.evaluations else 0.0
        top_display = f"{top_candidate} ({top_score}%)"

        highly_suitable_count = sum(1 for e in self.evaluations if e['total_score'] >= 90.0)

        return {
            'total_candidates': total_candidates,
            'average_score': avg_score,
            'top_candidate': top_display,
            'highly_suitable_count': highly_suitable_count
        }
