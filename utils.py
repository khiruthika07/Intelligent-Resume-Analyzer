"""
Intelligent Resume Analyzer - Utilities & Skill Taxonomy
Module containing text processing, normalization, and master skill taxonomy.
Uses ONLY Python Standard Library.
"""

import re
from typing import Dict, List, Set, Tuple

# Comprehensive Master Skill Taxonomy with canonical names and variations/aliases
SKILL_TAXONOMY: Dict[str, List[str]] = {
    # Programming Languages
    "Python": ["python", "py", "python3", "python2"],
    "Java": ["java", "j2ee", "core java"],
    "C": ["c language", "\\bc\\b"],
    "C++": ["c\\+\\+", "cpp", "c plus plus"],
    "C#": ["c#", "csharp", "c sharp"],
    "JavaScript": ["javascript", "js", "ecmascript", "es6"],
    "TypeScript": ["typescript", "ts"],
    "PHP": ["php"],
    "Ruby": ["ruby"],
    "Go": ["golang", "go language", "\\bgo\\b"],
    "Rust": ["rust"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin"],
    "R": ["r programming", "\\br\\b", "r-lang"],

    # Web Technologies & Frameworks
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "sass", "scss"],
    "React": ["react", "reactjs", "react.js", "react native"],
    "Node.js": ["node.js", "nodejs", "node"],
    "Express": ["express", "expressjs", "express.js"],
    "Angular": ["angular", "angularjs", "angular.js"],
    "Vue.js": ["vue", "vuejs", "vue.js"],
    "Django": ["django", "django rest framework"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi", "fast api"],
    "Bootstrap": ["bootstrap"],
    "Tailwind CSS": ["tailwind", "tailwindcss"],
    "REST API": ["rest api", "restful api", "restful", "rest apis"],
    "GraphQL": ["graphql"],

    # AI, ML & Data Science
    "Machine Learning": ["machine learning", "ml", "supervised learning", "unsupervised learning"],
    "Deep Learning": ["deep learning", "dl", "neural networks", "cnn", "rnn", "lstm", "transformers"],
    "Artificial Intelligence": ["artificial intelligence", "ai", "genai", "generative ai"],
    "Data Science": ["data science", "ds"],
    "Data Analysis": ["data analysis", "data analytics", "data analyst"],
    "Statistics": ["statistics", "statistical analysis", "probability", "hypothesis testing"],
    "Natural Language Processing": ["natural language processing", "nlp", "text mining"],
    "Computer Vision": ["computer vision", "cv", "opencv", "image processing"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "Scikit-Learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],

    # Data Tools & Visualization
    "Excel": ["excel", "ms excel", "microsoft excel", "vlookup", "pivot tables"],
    "Power BI": ["power bi", "powerbi", "dax"],
    "Tableau": ["tableau"],
    "Big Data": ["big data", "hadoop", "spark", "pyspark"],

    # Databases
    "SQL": ["sql", "structured query language"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo"],
    "Oracle": ["oracle", "oracle db"],
    "SQLite": ["sqlite", "sqlite3"],
    "Redis": ["redis"],

    # Cloud & DevOps
    "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "Azure": ["azure", "microsoft azure"],
    "Google Cloud Platform": ["gcp", "google cloud", "google cloud platform"],
    "Docker": ["docker", "containerization", "containers"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Git": ["git", "version control"],
    "GitHub": ["github", "gitlab", "bitbucket"],
    "CI/CD": ["ci/cd", "cicd", "continuous integration", "jenkins"],
    "Linux": ["linux", "ubuntu", "centos", "bash", "shell scripting", "unix"],
    "Cloud Computing": ["cloud computing", "cloud infrastructure"],
    "Cybersecurity": ["cybersecurity", "cyber security", "network security", "information security"],

    # Core Computer Science
    "Data Structures": ["data structures", "dsa", "arrays", "trees", "graphs", "linked lists"],
    "Algorithms": ["algorithms", "algo", "dynamic programming", "sorting algorithms"],
    "System Design": ["system design", "software architecture", "microservices"],
    "Microservices": ["microservices", "microservice architecture"],
    "Agile": ["agile", "scrum", "kanban"],

    # Soft Skills & Leadership
    "Communication": ["communication", "communication skills", "verbal communication", "written communication"],
    "Leadership": ["leadership", "team leadership", "management", "mentorship"],
    "Problem Solving": ["problem solving", "analytical thinking", "critical thinking", "troubleshooting"],
    "Teamwork": ["teamwork", "collaboration", "cross-functional collaboration"],
    "Time Management": ["time management", "prioritization", "multitasking"]
}

# Alias Map for Quick Standard Lookups
ALIAS_TO_CANONICAL: Dict[str, str] = {}
for canonical, aliases in SKILL_TAXONOMY.items():
    ALIAS_TO_CANONICAL[canonical.lower()] = canonical
    for alias in aliases:
        clean_alias = alias.replace("\\b", "").replace("\\+", "+").strip().lower()
        if clean_alias:
            ALIAS_TO_CANONICAL[clean_alias] = canonical

# General English Stop Words for Keyword Extraction
STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing",
    "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
    "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",
    "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no",
    "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves",
    "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to",
    "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
    "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves", "resume", "curriculum", "vitae", "profile",
    "summary", "work", "experience", "education", "skills", "project", "projects", "responsible", "duty",
    "duties", "building", "working", "using", "used", "etc", "e.g.", "i.e.", "role", "roles", "candidate",
    "applicant", "year", "years", "month", "months", "per", "description", "job", "requirement", "requirements"
}


def normalize_text(text: str) -> str:
    """Normalizes text by converting to lowercase and replacing non-standard whitespace."""
    if not text:
        return ""
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extracts canonical skill names from text using exact regex boundary matching
    and dictionary scanning.
    """
    if not text:
        return []

    normalized_lower = text.lower()
    found_skills: Set[str] = set()

    for canonical, aliases in SKILL_TAXONOMY.items():
        # Check canonical name first
        canon_pattern = r'(?:\b|_)' + re.escape(canonical.lower()) + r'(?:\b|_)'
        if re.search(canon_pattern, normalized_lower):
            found_skills.add(canonical)
            continue

        # Check aliases
        for alias in aliases:
            if alias.startswith("\\b") or alias.endswith("\\b"):
                pattern = alias
            else:
                pattern = r'(?:\b|_)' + re.escape(alias) + r'(?:\b|_)'
            try:
                if re.search(pattern, normalized_lower, re.IGNORECASE):
                    found_skills.add(canonical)
                    break
            except re.error:
                if alias.lower() in normalized_lower:
                    found_skills.add(canonical)
                    break

    # Additional standard acronym checks
    acronym_map = {
        r'\bml\b': "Machine Learning",
        r'\bdl\b': "Deep Learning",
        r'\bai\b': "Artificial Intelligence",
        r'\bds\b': "Data Science",
        r'\bnlp\b': "Natural Language Processing",
        r'\bcv\b': "Computer Vision",
        r'\bjs\b': "JavaScript",
        r'\bts\b': "TypeScript",
        r'\bdsa\b': "Data Structures",
        r'\bgcp\b': "Google Cloud Platform",
        r'\baws\b': "AWS"
    }

    for pattern, canonical in acronym_map.items():
        if re.search(pattern, normalized_lower):
            found_skills.add(canonical)

    return sorted(list(found_skills))


def extract_keywords_from_text(text: str, top_n: int = 20) -> List[str]:
    """Extracts top non-stop-word keywords and phrases from text."""
    if not text:
        return []

    clean_str = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    words = [w for w in clean_str.split() if len(w) > 2 and w not in STOP_WORDS]

    freq: Dict[str, int] = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    sorted_keywords = sorted(freq.keys(), key=lambda k: freq[k], reverse=True)
    return sorted_keywords[:top_n]
