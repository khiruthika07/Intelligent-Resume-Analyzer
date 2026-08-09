"""
Intelligent Resume Analyzer - Scoring Engine
Calculates dynamic weighted match scores (Skills 50%, Education 15%, Experience 20%, Keywords 15%)
and generates recommendations and detailed assessment reports.
Uses ONLY Python Standard Library.
"""

from typing import Dict, List, Any


class Scorer:
    """Evaluates candidate profiles against job descriptions using weighted scoring algorithm."""

    @staticmethod
    def calculate_score(candidate_profile: Dict[str, Any], jd_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates match scores and returns detailed breakdown:
        {
            'total_score': float, # 0 - 100
            'recommendation': str,
            'skills_score': float, # 0 - 100
            'education_score': float, # 0 - 100
            'experience_score': float, # 0 - 100
            'keyword_score': float, # 0 - 100
            'matched_skills': List[str],
            'missing_skills': List[str],
            'extra_skills': List[str],
            'assessment_summary': str
        }
        """
        cand_skills = set(candidate_profile.get('skills', []))
        jd_skills = set(jd_profile.get('required_skills', []))

        # 1. SKILLS SCORE (50% Weight)
        if jd_skills:
            matched_skills = sorted(list(cand_skills.intersection(jd_skills)))
            missing_skills = sorted(list(jd_skills.difference(cand_skills)))
            extra_skills = sorted(list(cand_skills.difference(jd_skills)))

            match_ratio = len(matched_skills) / len(jd_skills)
            base_skill_score = match_ratio * 100.0

            # Small bonus for relevant extra technical skills (up to 5 pts)
            extra_bonus = min(5.0, len(extra_skills) * 1.0)
            skills_score = min(100.0, base_skill_score + extra_bonus)
        else:
            matched_skills = sorted(list(cand_skills))
            missing_skills = []
            extra_skills = []
            skills_score = min(100.0, len(cand_skills) * 15.0)

        # 2. EDUCATION SCORE (15% Weight)
        education_score = Scorer._eval_education(
            candidate_profile.get('education_level', 'None'),
            jd_profile.get('required_education', 'Bachelor')
        )

        # 3. EXPERIENCE SCORE (20% Weight)
        cand_exp = float(candidate_profile.get('experience_years', 0.0))
        jd_exp = float(jd_profile.get('required_experience_years', 0.0))

        if jd_exp > 0:
            if cand_exp >= jd_exp:
                experience_score = 100.0
            else:
                experience_score = (cand_exp / jd_exp) * 100.0
        else:
            experience_score = 100.0 if cand_exp >= 1.0 else 80.0

        experience_score = min(100.0, max(0.0, experience_score))

        # 4. KEYWORD RELEVANCE SCORE (15% Weight)
        # Combine extracted keywords and skills for robust domain relevance matching
        cand_keywords = set(candidate_profile.get('keywords', [])).union(set(s.lower() for s in cand_skills))
        jd_keywords = set(jd_profile.get('keywords', [])).union(set(s.lower() for s in jd_skills))

        if jd_keywords:
            common_keywords = cand_keywords.intersection(jd_keywords)
            kw_match_ratio = len(common_keywords) / len(jd_keywords)
            keyword_score = min(100.0, kw_match_ratio * 150.0)  # scaled for overlap
        else:
            common_keywords = set()
            keyword_score = 70.0

        keyword_score = min(100.0, max(0.0, keyword_score))

        # COMPUTE FINAL WEIGHTED SCORE
        # Skills: 50%, Education: 15%, Experience: 20%, Keywords: 15%
        total_score = (
            (skills_score * 0.50) +
            (education_score * 0.15) +
            (experience_score * 0.20) +
            (keyword_score * 0.15)
        )
        total_score = round(min(100.0, max(0.0, total_score)), 1)

        # RECOMMENDATION CATEGORIES
        recommendation = Scorer._get_recommendation(total_score)

        # DYNAMIC ASSESSMENT GENERATION
        assessment_summary = Scorer._generate_assessment(
            candidate_name=candidate_profile.get('name', 'Candidate'),
            total_score=total_score,
            recommendation=recommendation,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            cand_exp=cand_exp,
            jd_exp=jd_exp,
            cand_edu=candidate_profile.get('education_level', 'None'),
            jd_edu=jd_profile.get('required_education', 'Bachelor')
        )

        return {
            'total_score': total_score,
            'recommendation': recommendation,
            'skills_score': round(skills_score, 1),
            'education_score': round(education_score, 1),
            'experience_score': round(experience_score, 1),
            'keyword_score': round(keyword_score, 1),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'extra_skills': extra_skills,
            'assessment_summary': assessment_summary
        }

    @staticmethod
    def _eval_education(cand_level: str, jd_level: str) -> float:
        """Compares candidate education rank against JD required education rank."""
        ranks = {
            'PhD': 4,
            'Master': 3,
            'Bachelor': 2,
            'Diploma': 1,
            'High School': 0,
            'None': 0
        }

        cand_rank = ranks.get(cand_level, 1)
        jd_rank = ranks.get(jd_level, 2)

        if cand_rank >= jd_rank:
            return 100.0
        elif cand_rank == jd_rank - 1:
            return 70.0
        elif cand_rank == jd_rank - 2:
            return 40.0
        else:
            return 20.0

    @staticmethod
    def _get_recommendation(score: float) -> str:
        """Maps final score to required recommendation categories."""
        if score >= 90.0:
            return "Highly Suitable"
        elif score >= 80.0:
            return "Suitable"
        elif score >= 70.0:
            return "Potential Candidate"
        elif score >= 50.0:
            return "Partially Suitable"
        else:
            return "Not Suitable"

    @staticmethod
    def _generate_assessment(
        candidate_name: str,
        total_score: float,
        recommendation: str,
        matched_skills: List[str],
        missing_skills: List[str],
        cand_exp: float,
        jd_exp: float,
        cand_edu: str,
        jd_edu: str
    ) -> str:
        """Generates dynamic human-readable explanation of candidate fit."""
        total_jd_skills = len(matched_skills) + len(missing_skills)

        if total_jd_skills > 0:
            skill_narrative = f"matches {len(matched_skills)} of {total_jd_skills} required skills ({', '.join(matched_skills[:4]) if matched_skills else 'None'})"
        else:
            skill_narrative = f"possesses technical skills ({', '.join(matched_skills[:4])})"

        if jd_exp > 0:
            if cand_exp >= jd_exp:
                exp_narrative = f"sufficient experience ({cand_exp:.1f} yrs vs {jd_exp:.1f} yrs required)"
            else:
                exp_narrative = f"below required experience ({cand_exp:.1f} yrs vs {jd_exp:.1f} yrs required)"
        else:
            exp_narrative = f"{cand_exp:.1f} years experience"

        edu_narrative = f"{cand_edu} degree qualification"

        if recommendation == "Highly Suitable":
            return (f"Outstanding candidate! {candidate_name} {skill_narrative}, "
                    f"possesses {exp_narrative}, and holds a {edu_narrative}. Highly recommended for immediate interview.")
        elif recommendation == "Suitable":
            return (f"Strong candidate. {candidate_name} {skill_narrative}, "
                    f"has {exp_narrative}, and meets {edu_narrative} requirements.")
        elif recommendation == "Potential Candidate":
            return (f"Promising candidate with potential. {candidate_name} {skill_narrative}, "
                    f"has {exp_narrative}. May require minor technical upskilling in missing skills ({', '.join(missing_skills[:3]) if missing_skills else 'N/A'}).")
        elif recommendation == "Partially Suitable":
            return (f"Partially suitable candidate. {candidate_name} {skill_narrative}, "
                    f"holds {exp_narrative}. Significant gap in key required skills ({', '.join(missing_skills[:4]) if missing_skills else 'N/A'}).")
        else:
            return (f"Unsuitable candidate. {candidate_name} lacks critical required skills ({', '.join(missing_skills[:5]) if missing_skills else 'multiple skills'}) "
                    f"and does not meet experience or qualification benchmarks.")
