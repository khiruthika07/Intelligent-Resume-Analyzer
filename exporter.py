"""
Intelligent Resume Analyzer - Data & Report Exporter
Exports screening results to CSV summary table and individual candidate TXT reports.
Uses ONLY Python Standard Library.
"""

import csv
import os
import re
from datetime import datetime
from typing import Dict, List, Any


class Exporter:
    """Handles CSV exports and TXT report generation for resume evaluations."""

    @staticmethod
    def export_to_csv(evaluations: List[Dict[str, Any]], output_path: str) -> str:
        """
        Exports candidate evaluation list to a clean CSV file.
        Returns the absolute path of created CSV file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        fieldnames = [
            'Rank', 'Candidate Name', 'Email', 'Phone', 'Final Score (%)',
            'Recommendation', 'Skills Score (%)', 'Education Score (%)',
            'Experience Score (%)', 'Keyword Score (%)', 'Matched Skills',
            'Missing Skills', 'Education Level', 'Experience (Yrs)', 'Assessment Summary'
        ]

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for eval_rec in evaluations:
                score_info = eval_rec['score_info']
                cand_profile = eval_rec['candidate_profile']

                writer.writerow({
                    'Rank': eval_rec.get('rank', '-'),
                    'Candidate Name': eval_rec['name'],
                    'Email': eval_rec['email'],
                    'Phone': eval_rec['phone'],
                    'Final Score (%)': eval_rec['total_score'],
                    'Recommendation': eval_rec['recommendation'],
                    'Skills Score (%)': score_info['skills_score'],
                    'Education Score (%)': score_info['education_score'],
                    'Experience Score (%)': score_info['experience_score'],
                    'Keyword Score (%)': score_info['keyword_score'],
                    'Matched Skills': ", ".join(score_info['matched_skills']),
                    'Missing Skills': ", ".join(score_info['missing_skills']),
                    'Education Level': cand_profile['education_level'],
                    'Experience (Yrs)': cand_profile['experience_years'],
                    'Assessment Summary': eval_rec['assessment_summary']
                })

        return output_path

    @staticmethod
    def export_individual_txt_report(eval_rec: Dict[str, Any], jd_profile: Dict[str, Any], output_dir: str) -> str:
        """
        Generates a comprehensive text report for a single candidate.
        Saves report into output_dir and returns path.
        """
        os.makedirs(output_dir, exist_ok=True)

        cand_profile = eval_rec['candidate_profile']
        score_info = eval_rec['score_info']

        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', cand_profile['name'].lower()).strip('_')
        filepath = os.path.join(output_dir, f"{safe_name}_screening_report.txt")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_content = f"""================================================================================
                      INTELLIGENT RESUME ANALYZER
                       CANDIDATE SCREENING REPORT
================================================================================
Generated On       : {timestamp}
Job Position       : {jd_profile.get('title', 'Job Description')}
Candidate Name     : {cand_profile['name']}
Email Address      : {cand_profile['email']}
Phone Number       : {cand_profile['phone']}
--------------------------------------------------------------------------------
OVERALL MATCH EVALUATION
--------------------------------------------------------------------------------
Rank Position      : #{eval_rec.get('rank', 1)}
Final Match Score  : {eval_rec['total_score']}%
Recommendation     : {eval_rec['recommendation']}

COMPONENT SCORE BREAKDOWN (WEIGHTED)
--------------------------------------------------------------------------------
1. Skills Match (50% Weight)       : {score_info['skills_score']}%
2. Education Match (15% Weight)    : {score_info['education_score']}%
3. Experience Match (20% Weight)   : {score_info['experience_score']}%
4. Keyword Relevance (15% Weight)  : {score_info['keyword_score']}%

SKILLS ANALYSIS
--------------------------------------------------------------------------------
JD Required Skills : {", ".join(jd_profile.get('required_skills', [])) if jd_profile.get('required_skills') else 'None Specified'}
Matched Skills ({len(score_info['matched_skills'])})  : {", ".join(score_info['matched_skills']) if score_info['matched_skills'] else 'None'}
Missing Skills ({len(score_info['missing_skills'])})  : {", ".join(score_info['missing_skills']) if score_info['missing_skills'] else 'None'}
Extra Skills        : {", ".join(score_info['extra_skills']) if score_info['extra_skills'] else 'None'}

QUALIFICATIONS & EXPERIENCE
--------------------------------------------------------------------------------
Required Education : {jd_profile.get('required_education', 'Bachelor')}
Candidate Degree   : {cand_profile['education_level']} ({cand_profile['education_details']})

Required Experience: {jd_profile.get('required_experience_years', 0.0)} Years
Candidate Exp      : {cand_profile['experience_years']} Years ({cand_profile['experience_details']})

EXECUTIVE ASSESSMENT SUMMARY
--------------------------------------------------------------------------------
{eval_rec['assessment_summary']}

================================================================================
              CONFIDENTIAL • INTELLIGENT RESUME ANALYZER REPORT
================================================================================
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return filepath
