# 🎯 INTELLIGENT RESUME ANALYZER
> **Smart Candidate Screening • Faster Decisions • Better Hiring**

A premium, production-quality offline resume screening application built using **Python 3 + Tkinter + Python Standard Library ONLY**.

---

## 📌 Problem Statement
Recruitment teams receive hundreds of resumes for every job opening. Manually reading each resume to verify technical skills, years of experience, and educational qualifications is time-consuming, inconsistent, and prone to human bias. Existing AI services often require expensive subscriptions, cloud dependencies, or active internet connectivity, creating privacy and compliance risks when handling sensitive personal candidate data.

## 🎯 Objective
**INTELLIGENT RESUME ANALYZER** provides a fast, transparent, privacy-first, and completely offline recruitment tool. It compares multiple candidate resumes (`.txt` format) against a target Job Description (JD), calculates a dynamic weighted match score, ranks candidates in real-time, and generates human-readable executive fit reports.

---

## ✨ Features

- 📄 **Job Description Parsing**: Automatically extracts required technical skills, minimum experience years, education qualifications, and key domain keywords from any pasted or uploaded JD.
- 📂 **Multi-Resume Batch Upload**: Add and process multiple candidate `.txt` resumes simultaneously.
- 🔍 **Taxonomy-Driven Skill Extraction**: Recognizes over 40+ technologies across domains (Languages, Web, AI/ML, Cloud, Databases, Core CS, Soft Skills) with alias variation support (`ML` → `Machine Learning`, `JS` → `JavaScript`, `ReactJS` → `React`, `PowerBI` → `Power BI`, etc.).
- 📊 **Dynamic Weighted Match Scoring**: Transparent, non-hardcoded evaluation algorithm (Skills 50%, Education 15%, Experience 20%, Keyword Relevance 15%).
- 🏆 **Automatic Candidate Ranking**: Ranks candidates in descending order of overall suitability.
- 🏷️ **Recommendation Tiering**:
  - `90–100%`: **Highly Suitable**
  - `80–89%`: **Suitable**
  - `70–79%`: **Potential Candidate**
  - `50–69%`: **Partially Suitable**
  - `< 50%`: **Not Suitable**
- 👤 **Detailed Candidate Profile Popup**: Interactive modal window showing matched vs. missing skills, progress bars for each weighted metric, and a dynamic executive summary text.
- 📥 **CSV Summary Export**: One-click export of complete candidate rankings table to CSV for spreadsheet integration.
- 📄 **TXT Individual Reports**: Saves professional, timestamped candidate screening reports to `results/reports/`.
- 💎 **Luxury Dark Theme UI**: Designed with a charcoal palette (`#121212`), metallic gold accents (`#D4AF37`), stat metric cards, styled `Treeview` tables, and custom progress bars.

---

## 🛠️ Technologies Used

- **Language**: Python 3.8+
- **GUI Framework**: Tkinter (Standard Library `tkinter`, `ttk`, `filedialog`, `messagebox`)
- **Text Processing & Math**: Standard Modules (`re`, `csv`, `json`, `os`, `sys`, `pathlib`, `collections`, `datetime`)
- **Dependencies**: **ZERO pip / external packages required!** Completely offline and self-contained.

---

## ⚙️ How It Works

```
┌─────────────────┐       ┌────────────────────┐
│ Job Description │       │ Candidate Resumes  │
└────────┬────────┘       └─────────┬──────────┘
         │                          │
         ▼                          ▼
 ┌──────────────┐          ┌─────────────────┐
 │  JD Parser   │          │  Resume Parser  │
 └───────┬──────┘          └────────┬────────┘
         │                          │
         └───────────┬──────────────┘
                     ▼
           ┌──────────────────┐
           │  Scoring Engine  │
           └─────────┬────────┘
                     │
                     ▼
           ┌──────────────────┐
           │ Dashboard & GUI  │
           └──────────────────┘
```

1. **Input Stage**: The user pastes/loads a Job Description and uploads `.txt` candidate resumes.
2. **Parsing Stage**:
   - `jd_parser.py` extracts required skills, experience requirement (years), and education level.
   - `resume_parser.py` extracts candidate contact info (Name, Email, Phone), detected skills, education qualification, and work experience years.
3. **Scoring Stage**: `scorer.py` evaluates every resume against the parsed JD using the transparent weighted mathematical formula.
4. **Presentation & Export Stage**: `gui.py` displays live dashboard stat metrics, populates ranked candidate tables, allows candidate detail inspection, and enables CSV / TXT report export via `exporter.py`.

---

## 📐 Weighted Scoring Algorithm

$$ \text{Final Score} = (\text{Skills Score} \times 0.50) + (\text{Experience Score} \times 0.20) + (\text{Education Score} \times 0.15) + (\text{Keyword Score} \times 0.15) $$

1. **Skills Score (50%)**:
   - $\text{Match Ratio} = \frac{\text{Count}(\text{Matched Skills})}{\text{Count}(\text{JD Skills})} \times 100$
   - Extra credit (+1 pt per relevant extra skill, max +5 pts bonus).
2. **Experience Score (20%)**:
   - If Candidate Exp $\ge$ JD Required Exp $\rightarrow 100\%$.
   - If Candidate Exp $<$ JD Required Exp $\rightarrow \left( \frac{\text{Candidate Exp}}{\text{JD Required Exp}} \right) \times 100\%$.
3. **Education Score (15%)**:
   - Degree Hierarchy: PhD (4) > Master (3) > Bachelor (2) > Diploma (1) > High School (0).
   - Candidate level $\ge$ JD required level $\rightarrow 100\%$.
   - 1 level below $\rightarrow 70\%$, 2 levels below $\rightarrow 40\%$.
4. **Keyword Relevance Score (15%)**:
   - Jaccard similarity ratio of top non-stop-word domain terms between candidate text and JD text.

---

## 🚀 Quick Run Instructions

### Prerequisites
- Installed **Python 3.8** or higher (with Tkinter enabled, included by default in standard Python installations).

### Execution
Run the application with a single command:

```bash
python main.py
```

### Quick Demo Flow
1. Click **`⚡ Load Sample Data`** in the top header.
2. The application automatically loads `data/sample_jd.txt` and 5 realistic sample candidate resumes (`anjali_kumar.txt`, `rahul_raj.txt`, `priya_sharma.txt`, `arun_kumar.txt`, `meena_s.txt`).
3. View the live ranked evaluation table and updated dashboard stat cards.
4. Double-click any candidate row or click **`🔍 View Candidate Details`** to inspect the candidate breakdown window.
5. Click **`📥 Export CSV`** or **`📁 Save All Reports`** to test report generation into the `results/` directory.

---

## 📁 Project Structure

```text
Intelligent-Resume-Analyzer/
├── main.py                # Main application entry point
├── gui.py                 # Luxury dark theme desktop GUI implementation
├── analyzer.py            # Main pipeline controller & dashboard metrics
├── resume_parser.py       # Extractor for candidate contact info, skills, edu, exp
├── jd_parser.py           # Extractor for job description requirements
├── scorer.py              # Transparent weighted scoring engine & recommendation logic
├── exporter.py            # Exporter for CSV summaries & TXT candidate reports
├── utils.py               # Master skill taxonomy, alias mappings, & text cleaning
├── data/                  # Bundled datasets
│   ├── sample_jd.txt      # Sample Job Description (Senior AI & Python Engineer)
│   └── sample_resumes/    # Realistic sample candidate resumes
│       ├── anjali_kumar.txt  # Score ~92-96% (Highly Suitable)
│       ├── rahul_raj.txt     # Score ~82-86% (Suitable)
│       ├── priya_sharma.txt  # Score ~71-76% (Potential Candidate)
│       ├── arun_kumar.txt    # Score ~54-60% (Partially Suitable)
│       └── meena_s.txt       # Score ~30-38% (Not Suitable)
├── results/               # Generated CSV summaries & TXT reports
│   └── reports/
├── README.md              # Project documentation
├── requirements.txt       # Requirements & stdlib compatibility notice
└── .gitignore             # Standard gitignore rules
```

---

## ⚠️ Limitations & Future Enhancements

### Current Limitations
- Supports `.txt` resume files. (PDF and DOCX formats are avoided to strictly maintain zero external pip dependency requirement).
- Keyword matching relies on tokenization and dictionary taxonomy matching rather than deep semantic contextual embeddings.

### Future Enhancements
- 📄 Add native pure-Python PDF/DOCX stream decoders.
- 🎨 Provide customizable UI theme pickers (Dark Luxury Gold, Clean Minimal White, Cyberpunk Slate).
- 📈 Multi-Job comparison (analyzing candidates across multiple open roles simultaneously).

---

## 📜 License
Developed as an open, offline academic & recruitment software project. Built with Python 3 Standard Library.
