"""
Intelligent Resume Analyzer - Luxury Dark Theme GUI
Modern, production-grade desktop interface using Python 3 + Tkinter + Standard Library ONLY.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, List, Any, Optional

from analyzer import ResumeAnalyzer
from exporter import Exporter


class LuxuryTheme:
    """Luxury Dark Color Palette and Typography Constants."""
    BG_DARK = "#121212"          # Deep Charcoal Window Background
    CARD_BG = "#1E1E1E"          # Lighter Dark Card Background
    CARD_BORDER = "#2A2A2A"      # Card Subtle Border
    INPUT_BG = "#181818"         # Text Box / Input Field Background
    INPUT_FG = "#F0F0F0"         # Input Text Color
    
    # Gold Accents
    GOLD_PRIMARY = "#D4AF37"     # Elegance Gold
    GOLD_HOVER = "#E5C158"       # Lighter Gold for Hover
    GOLD_DARK = "#A3821A"        # Deep Gold
    GOLD_TEXT = "#FFD700"        # Bright Gold Text Accent
    
    # Text Colors
    TEXT_PRIMARY = "#FFFFFF"     # Crisp White Headings
    TEXT_SECONDARY = "#E0E0E0"   # Body Text
    TEXT_MUTED = "#9E9E9E"       # Muted Labels / Subtitles
    
    # Recommendation Badges & Tiers
    COLOR_HIGHLY_SUITABLE = "#FFD700"  # Gold
    BG_HIGHLY_SUITABLE = "#3A3000"
    
    COLOR_SUITABLE = "#00E676"         # Emerald Green
    BG_SUITABLE = "#00381B"
    
    COLOR_POTENTIAL = "#00E5FF"        # Cyan/Blue
    BG_POTENTIAL = "#003344"
    
    COLOR_PARTIAL = "#FFB300"          # Amber/Yellow
    BG_PARTIAL = "#3A2800"
    
    COLOR_UNSUITABLE = "#FF5252"       # Coral Red
    BG_UNSUITABLE = "#380000"
    
    # Fonts
    FONT_FAMILY = "Segoe UI" if os.name == 'nt' else "Helvetica"
    FONT_TITLE = (FONT_FAMILY, 18, "bold")
    FONT_SUBTITLE = (FONT_FAMILY, 10, "normal")
    FONT_HEADER = (FONT_FAMILY, 12, "bold")
    FONT_BODY = (FONT_FAMILY, 10, "normal")
    FONT_BOLD = (FONT_FAMILY, 10, "bold")
    FONT_STAT_VAL = (FONT_FAMILY, 18, "bold")
    FONT_STAT_LBL = (FONT_FAMILY, 9, "bold")


class IntelligentResumeAnalyzerGUI:
    """Main Application GUI Class for Intelligent Resume Analyzer."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("INTELLIGENT RESUME ANALYZER - Luxury Recruitment Suite")
        self.root.geometry("1280x820")
        self.root.minsize(1100, 700)
        self.root.configure(bg=LuxuryTheme.BG_DARK)

        self.analyzer = ResumeAnalyzer()
        self.uploaded_resume_paths: List[str] = []

        # Configure custom TTK styles
        self._setup_ttk_styles()

        # Build Main UI Layout
        self._build_header()
        self._build_main_layout()

        # Bind Shortcuts & Events
        self.root.bind("<Control-o>", lambda e: self.load_jd_file())
        self.root.bind("<Control-u>", lambda e: self.add_resumes())
        self.root.bind("<Control-r>", lambda e: self.run_analysis())

    def _setup_ttk_styles(self):
        """Configures custom dark theme TTK styles for Treeview, Buttons, and Scrollbars."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Treeview Styling
        self.style.configure(
            "Dark.Treeview",
            background=LuxuryTheme.CARD_BG,
            foreground=LuxuryTheme.TEXT_SECONDARY,
            fieldbackground=LuxuryTheme.CARD_BG,
            rowheight=34,
            font=LuxuryTheme.FONT_BODY,
            borderwidth=0
        )
        self.style.map(
            "Dark.Treeview",
            background=[("selected", "#2C2C2E")],
            foreground=[("selected", LuxuryTheme.GOLD_TEXT)]
        )

        # Treeview Header Styling
        self.style.configure(
            "Dark.Treeview.Heading",
            background="#181818",
            foreground=LuxuryTheme.GOLD_PRIMARY,
            font=LuxuryTheme.FONT_HEADER,
            borderwidth=1,
            relief="flat"
        )
        self.style.map(
            "Dark.Treeview.Heading",
            background=[("active", "#252525")]
        )

        # Progressbar Styling
        self.style.configure(
            "Gold.Horizontal.TProgressbar",
            troughcolor="#181818",
            background=LuxuryTheme.GOLD_PRIMARY,
            thickness=12,
            borderwidth=0
        )

    def _build_header(self):
        """Builds top header banner with title, subtitle, and action buttons."""
        header_frame = tk.Frame(self.root, bg=LuxuryTheme.CARD_BG, height=75, highlightbackground=LuxuryTheme.CARD_BORDER, highlightthickness=1)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=12, pady=(12, 6))
        header_frame.pack_propagate(False)

        # Title & Subtitle Container
        title_box = tk.Frame(header_frame, bg=LuxuryTheme.CARD_BG)
        title_box.pack(side=tk.LEFT, padx=16, pady=8)

        title_label = tk.Label(
            title_box,
            text="🎯 INTELLIGENT RESUME ANALYZER",
            font=LuxuryTheme.FONT_TITLE,
            fg=LuxuryTheme.GOLD_TEXT,
            bg=LuxuryTheme.CARD_BG
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            title_box,
            text="Smart Candidate Screening  •  Faster Decisions  •  Better Hiring",
            font=LuxuryTheme.FONT_SUBTITLE,
            fg=LuxuryTheme.TEXT_MUTED,
            bg=LuxuryTheme.CARD_BG
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # Top Action Buttons (Right Aligned)
        btn_box = tk.Frame(header_frame, bg=LuxuryTheme.CARD_BG)
        btn_box.pack(side=tk.RIGHT, padx=16)

        btn_sample = tk.Button(
            btn_box,
            text="⚡ Load Sample Data",
            font=LuxuryTheme.FONT_BOLD,
            fg=LuxuryTheme.GOLD_TEXT,
            bg="#262214",
            activebackground="#3A321B",
            activeforeground="#FFFFFF",
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.load_sample_data
        )
        btn_sample.pack(side=tk.LEFT, padx=6)

        btn_csv = tk.Button(
            btn_box,
            text="📥 Export CSV",
            font=LuxuryTheme.FONT_BOLD,
            fg=LuxuryTheme.TEXT_PRIMARY,
            bg="#252525",
            activebackground="#333333",
            activeforeground="#FFFFFF",
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.export_csv_summary
        )
        btn_csv.pack(side=tk.LEFT, padx=6)

        btn_reset = tk.Button(
            btn_box,
            text="🔄 Reset",
            font=LuxuryTheme.FONT_BOLD,
            fg=LuxuryTheme.TEXT_MUTED,
            bg="#1E1E1E",
            activebackground="#2E2E2E",
            activeforeground="#FFFFFF",
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.reset_all
        )
        btn_reset.pack(side=tk.LEFT, padx=6)

    def _build_main_layout(self):
        """Builds two-column responsive main workspace layout."""
        main_container = tk.Frame(self.root, bg=LuxuryTheme.BG_DARK)
        main_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        # LEFT COLUMN (Job Description & Resumes Management)
        left_col = tk.Frame(main_container, bg=LuxuryTheme.BG_DARK, width=420)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 6))
        left_col.pack_propagate(False)

        # 1. Job Description Section Card
        jd_card = tk.LabelFrame(
            left_col,
            text=" 📄 JOB DESCRIPTION ",
            font=LuxuryTheme.FONT_HEADER,
            fg=LuxuryTheme.GOLD_PRIMARY,
            bg=LuxuryTheme.CARD_BG,
            bd=1,
            relief="solid",
            labelanchor="nw"
        )
        jd_card.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        # JD Controls Subframe
        jd_btn_frame = tk.Frame(jd_card, bg=LuxuryTheme.CARD_BG)
        jd_btn_frame.pack(fill=tk.X, padx=10, pady=(6, 4))

        btn_load_jd = tk.Button(
            jd_btn_frame,
            text="📁 Open JD File",
            font=LuxuryTheme.FONT_BODY,
            fg=LuxuryTheme.TEXT_PRIMARY,
            bg="#2A2A2A",
            activebackground="#3A3A3A",
            bd=0,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self.load_jd_file
        )
        btn_load_jd.pack(side=tk.LEFT)

        btn_clear_jd = tk.Button(
            jd_btn_frame,
            text="Clear",
            font=LuxuryTheme.FONT_BODY,
            fg=LuxuryTheme.TEXT_MUTED,
            bg=LuxuryTheme.CARD_BG,
            activebackground="#2A2A2A",
            bd=0,
            padx=6,
            pady=3,
            cursor="hand2",
            command=self.clear_jd
        )
        btn_clear_jd.pack(side=tk.RIGHT)

        # JD Text Area
        jd_text_container = tk.Frame(jd_card, bg=LuxuryTheme.INPUT_BG, bd=1, relief="solid")
        jd_text_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        self.jd_text_area = tk.Text(
            jd_text_container,
            wrap=tk.WORD,
            font=LuxuryTheme.FONT_BODY,
            bg=LuxuryTheme.INPUT_BG,
            fg=LuxuryTheme.INPUT_FG,
            insertbackground=LuxuryTheme.GOLD_PRIMARY,
            bd=0,
            padx=6,
            pady=6
        )
        self.jd_text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        jd_scroll = tk.Scrollbar(jd_text_container, command=self.jd_text_area.yview, bg=LuxuryTheme.CARD_BG)
        jd_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.jd_text_area.config(yscrollcommand=jd_scroll.set)

        # JD Summary Tags Label
        self.jd_summary_lbl = tk.Label(
            jd_card,
            text="Required Skills: None Detected",
            font=LuxuryTheme.FONT_SUBTITLE,
            fg=LuxuryTheme.TEXT_MUTED,
            bg=LuxuryTheme.CARD_BG,
            anchor="w",
            padx=10,
            pady=4
        )
        self.jd_summary_lbl.pack(fill=tk.X)

        # 2. Resumes List Section Card
        res_card = tk.LabelFrame(
            left_col,
            text=" 📂 CANDIDATE RESUMES (.TXT) ",
            font=LuxuryTheme.FONT_HEADER,
            fg=LuxuryTheme.GOLD_PRIMARY,
            bg=LuxuryTheme.CARD_BG,
            bd=1,
            relief="solid",
            labelanchor="nw"
        )
        res_card.pack(fill=tk.BOTH, expand=True, pady=6)

        res_btn_frame = tk.Frame(res_card, bg=LuxuryTheme.CARD_BG)
        res_btn_frame.pack(fill=tk.X, padx=10, pady=(6, 4))

        btn_add_res = tk.Button(
            res_btn_frame,
            text="➕ Upload .txt Resumes",
            font=LuxuryTheme.FONT_BOLD,
            fg=LuxuryTheme.GOLD_TEXT,
            bg="#262214",
            activebackground="#3A321B",
            bd=1,
            relief="solid",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.add_resumes
        )
        btn_add_res.pack(side=tk.LEFT)

        btn_clear_res = tk.Button(
            res_btn_frame,
            text="Clear All",
            font=LuxuryTheme.FONT_BODY,
            fg=LuxuryTheme.TEXT_MUTED,
            bg=LuxuryTheme.CARD_BG,
            activebackground="#2A2A2A",
            bd=0,
            padx=6,
            pady=3,
            cursor="hand2",
            command=self.clear_resumes
        )
        btn_clear_res.pack(side=tk.RIGHT)

        # Resumes Listbox
        list_container = tk.Frame(res_card, bg=LuxuryTheme.INPUT_BG, bd=1, relief="solid")
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        self.resumes_listbox = tk.Listbox(
            list_container,
            font=LuxuryTheme.FONT_BODY,
            bg=LuxuryTheme.INPUT_BG,
            fg=LuxuryTheme.INPUT_FG,
            selectbackground="#2C2C2E",
            selectforeground=LuxuryTheme.GOLD_TEXT,
            bd=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.resumes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)

        list_scroll = tk.Scrollbar(list_container, command=self.resumes_listbox.yview, bg=LuxuryTheme.CARD_BG)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.resumes_listbox.config(yscrollcommand=list_scroll.set)

        self.resume_count_lbl = tk.Label(
            res_card,
            text="Total Resumes Loaded: 0",
            font=LuxuryTheme.FONT_SUBTITLE,
            fg=LuxuryTheme.TEXT_MUTED,
            bg=LuxuryTheme.CARD_BG,
            anchor="w",
            padx=10,
            pady=4
        )
        self.resume_count_lbl.pack(fill=tk.X)

        # PROMINENT MAIN CALL TO ACTION BUTTON
        btn_analyze = tk.Button(
            left_col,
            text="🚀 ANALYZE CANDIDATES",
            font=(LuxuryTheme.FONT_FAMILY, 13, "bold"),
            fg="#000000",
            bg=LuxuryTheme.GOLD_PRIMARY,
            activebackground=LuxuryTheme.GOLD_HOVER,
            activeforeground="#000000",
            bd=0,
            relief="flat",
            pady=10,
            cursor="hand2",
            command=self.run_analysis
        )
        btn_analyze.pack(fill=tk.X, pady=(6, 0))

        # RIGHT COLUMN (Dashboard, Stat Cards & Ranked Table)
        right_col = tk.Frame(main_container, bg=LuxuryTheme.BG_DARK)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 1. Stat Cards Row
        stat_frame = tk.Frame(right_col, bg=LuxuryTheme.BG_DARK)
        stat_frame.pack(fill=tk.X, pady=(0, 8))

        self.card_total = self._create_stat_card(stat_frame, "CANDIDATES ANALYZED", "0", "👥")
        self.card_avg = self._create_stat_card(stat_frame, "AVERAGE MATCH SCORE", "0.0%", "📊")
        self.card_top = self._create_stat_card(stat_frame, "TOP CANDIDATE", "None", "🏆")
        self.card_suitable = self._create_stat_card(stat_frame, "HIGHLY SUITABLE", "0", "⭐")

        # 2. Ranked Candidate Results Table Card
        table_card = tk.LabelFrame(
            right_col,
            text=" 🏆 RANKED CANDIDATES EVALUATION ",
            font=LuxuryTheme.FONT_HEADER,
            fg=LuxuryTheme.GOLD_PRIMARY,
            bg=LuxuryTheme.CARD_BG,
            bd=1,
            relief="solid",
            labelanchor="nw"
        )
        table_card.pack(fill=tk.BOTH, expand=True)

        # Treeview Scroll Container
        tree_container = tk.Frame(table_card, bg=LuxuryTheme.CARD_BG)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("rank", "name", "score", "skills", "experience", "recommendation")
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            style="Dark.Treeview",
            selectmode="browse"
        )

        self.tree.heading("rank", text="Rank")
        self.tree.heading("name", text="Candidate Name")
        self.tree.heading("score", text="Score (%)")
        self.tree.heading("skills", text="Skill Match")
        self.tree.heading("experience", text="Experience")
        self.tree.heading("recommendation", text="Recommendation")

        self.tree.column("rank", width=60, anchor="center")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("score", width=100, anchor="center")
        self.tree.column("skills", width=220, anchor="w")
        self.tree.column("experience", width=110, anchor="center")
        self.tree.column("recommendation", width=160, anchor="center")

        tree_vscroll = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_vscroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_vscroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Double Click Event for Candidate Profile Details
        self.tree.bind("<Double-1>", lambda e: self.open_candidate_detail())

        # Bottom Action Bar inside Table Card
        action_bar = tk.Frame(table_card, bg=LuxuryTheme.CARD_BG)
        action_bar.pack(fill=tk.X, padx=10, pady=(0, 10))

        btn_detail = tk.Button(
            action_bar,
            text="🔍 View Candidate Details",
            font=LuxuryTheme.FONT_BOLD,
            fg=LuxuryTheme.GOLD_TEXT,
            bg="#262214",
            activebackground="#3A321B",
            bd=1,
            relief="solid",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.open_candidate_detail
        )
        btn_detail.pack(side=tk.LEFT, padx=(0, 8))

        btn_report = tk.Button(
            action_bar,
            text="📄 Save TXT Report",
            font=LuxuryTheme.FONT_BOLD,
            fg=LuxuryTheme.TEXT_PRIMARY,
            bg="#252525",
            activebackground="#333333",
            bd=1,
            relief="solid",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.export_single_report
        )
        btn_report.pack(side=tk.LEFT, padx=4)

        btn_all_reports = tk.Button(
            action_bar,
            text="📁 Save All Reports",
            font=LuxuryTheme.FONT_BODY,
            fg=LuxuryTheme.TEXT_MUTED,
            bg=LuxuryTheme.CARD_BG,
            activebackground="#2A2A2A",
            bd=1,
            relief="solid",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.export_all_reports
        )
        btn_all_reports.pack(side=tk.RIGHT)

    def _create_stat_card(self, parent: tk.Frame, title: str, default_val: str, icon: str) -> tk.Label:
        """Creates a modern dark metric stat card component."""
        card = tk.Frame(
            parent,
            bg=LuxuryTheme.CARD_BG,
            highlightbackground=LuxuryTheme.CARD_BORDER,
            highlightthickness=1,
            bd=0
        )
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        header_box = tk.Frame(card, bg=LuxuryTheme.CARD_BG)
        header_box.pack(fill=tk.X, padx=10, pady=(8, 2))

        icon_lbl = tk.Label(header_box, text=icon, font=(LuxuryTheme.FONT_FAMILY, 12), bg=LuxuryTheme.CARD_BG)
        icon_lbl.pack(side=tk.LEFT)

        lbl_title = tk.Label(
            header_box,
            text=f" {title}",
            font=LuxuryTheme.FONT_STAT_LBL,
            fg=LuxuryTheme.TEXT_MUTED,
            bg=LuxuryTheme.CARD_BG
        )
        lbl_title.pack(side=tk.LEFT)

        val_lbl = tk.Label(
            card,
            text=default_val,
            font=LuxuryTheme.FONT_STAT_VAL,
            fg=LuxuryTheme.GOLD_TEXT,
            bg=LuxuryTheme.CARD_BG
        )
        val_lbl.pack(anchor="w", padx=12, pady=(0, 8))

        return val_lbl

    # ================= EVENT HANDLERS & LOGIC =================

    def load_jd_file(self):
        """Opens file dialog to select a Job Description .txt file."""
        path = filedialog.askopenfilename(
            title="Select Job Description File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                self.jd_text_area.delete("1.0", tk.END)
                self.jd_text_area.insert(tk.END, content)
                self._on_jd_updated()
            except Exception as e:
                messagebox.showerror("Error Reading File", f"Could not read JD file:\n{e}")

    def clear_jd(self):
        """Clears JD text area."""
        self.jd_text_area.delete("1.0", tk.END)
        self.jd_summary_lbl.config(text="Required Skills: None Detected", fg=LuxuryTheme.TEXT_MUTED)

    def add_resumes(self):
        """Opens file dialog to upload multiple .txt resume files."""
        paths = filedialog.askopenfilenames(
            title="Select Candidate Resume Files (.txt)",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if paths:
            added = 0
            for p in paths:
                if p not in self.uploaded_resume_paths:
                    self.uploaded_resume_paths.append(p)
                    fname = os.path.basename(p)
                    self.resumes_listbox.insert(tk.END, f"📄 {fname}")
                    added += 1
            self.resume_count_lbl.config(
                text=f"Total Resumes Loaded: {len(self.uploaded_resume_paths)}",
                fg=LuxuryTheme.GOLD_TEXT if self.uploaded_resume_paths else LuxuryTheme.TEXT_MUTED
            )

    def clear_resumes(self):
        """Clears uploaded resumes list."""
        self.uploaded_resume_paths = []
        self.resumes_listbox.delete(0, tk.END)
        self.resume_count_lbl.config(text="Total Resumes Loaded: 0", fg=LuxuryTheme.TEXT_MUTED)

    def load_sample_data(self):
        """Loads default bundled sample JD and 5 sample resumes."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sample_jd_path = os.path.join(base_dir, "data", "sample_jd.txt")
        sample_resumes_dir = os.path.join(base_dir, "data", "sample_resumes")

        if not os.path.exists(sample_jd_path) or not os.path.exists(sample_resumes_dir):
            messagebox.showerror("Sample Data Missing", f"Could not locate sample files at:\n{sample_jd_path}")
            return

        # Load JD
        with open(sample_jd_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        self.jd_text_area.delete("1.0", tk.END)
        self.jd_text_area.insert(tk.END, jd_text)
        self._on_jd_updated()

        # Load Resumes
        self.clear_resumes()
        sample_files = [
            os.path.join(sample_resumes_dir, fname)
            for fname in os.listdir(sample_resumes_dir)
            if fname.endswith(".txt")
        ]

        for p in sorted(sample_files):
            self.uploaded_resume_paths.append(p)
            self.resumes_listbox.insert(tk.END, f"📄 {os.path.basename(p)}")

        self.resume_count_lbl.config(
            text=f"Total Resumes Loaded: {len(self.uploaded_resume_paths)}",
            fg=LuxuryTheme.GOLD_TEXT
        )

        # Run analysis immediately for demo smoothness
        self.run_analysis()

    def _on_jd_updated(self):
        """Parses JD text and updates preview label."""
        jd_content = self.jd_text_area.get("1.0", tk.END).strip()
        if jd_content:
            jd_profile = self.analyzer.set_job_description(jd_content)
            req_skills = jd_profile.get('required_skills', [])
            skills_str = ", ".join(req_skills) if req_skills else "General Profile"
            exp_str = f"{jd_profile.get('required_experience_years', 0.0)} yrs"
            self.jd_summary_lbl.config(
                text=f"Skills ({len(req_skills)}): {skills_str[:45]}... | Req Exp: {exp_str}",
                fg=LuxuryTheme.GOLD_PRIMARY
            )

    def run_analysis(self):
        """Executes candidate screening evaluation pipeline."""
        jd_content = self.jd_text_area.get("1.0", tk.END).strip()
        if not jd_content:
            messagebox.showwarning("Missing Input", "Please paste or load a Job Description first.")
            return

        if not self.uploaded_resume_paths:
            messagebox.showwarning("Missing Input", "Please upload at least one candidate resume (.txt).")
            return

        try:
            # Parse JD
            self.analyzer.set_job_description(jd_content)

            # Analyze Resumes
            evaluations = self.analyzer.analyze_resumes(self.uploaded_resume_paths)

            # Update Dashboard Table
            self._update_table(evaluations)

            # Update Dashboard Stat Cards
            stats = self.analyzer.get_dashboard_stats()
            self.card_total.config(text=str(stats['total_candidates']))
            self.card_avg.config(text=f"{stats['average_score']}%")
            self.card_top.config(text=stats['top_candidate'])
            self.card_suitable.config(text=str(stats['highly_suitable_count']))

        except Exception as e:
            messagebox.showerror("Analysis Error", f"An error occurred during evaluation:\n{e}")

    def _update_table(self, evaluations: List[Dict[str, Any]]):
        """Populates Treeview table with ranked evaluations."""
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        for eval_rec in evaluations:
            score_info = eval_rec['score_info']
            cand_profile = eval_rec['candidate_profile']

            matched_cnt = len(score_info['matched_skills'])
            total_req = matched_cnt + len(score_info['missing_skills'])
            skills_display = f"{matched_cnt}/{total_req} Matched ({', '.join(score_info['matched_skills'][:2])})" if total_req > 0 else f"{matched_cnt} Skills"

            exp_display = f"{cand_profile['experience_years']} Yrs"

            item_id = self.tree.insert(
                "",
                tk.END,
                values=(
                    f"#{eval_rec['rank']}",
                    eval_rec['name'],
                    f"{eval_rec['total_score']}%",
                    skills_display,
                    exp_display,
                    eval_rec['recommendation']
                )
            )

    def open_candidate_detail(self):
        """Opens popup modal window displaying detailed candidate profile analysis."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Candidate", "Please select a candidate row from the table to view details.")
            return

        item = self.tree.item(selected[0])
        values = item['values']
        if not values or not self.analyzer.evaluations:
            return

        # Find evaluation matching rank
        rank_str = str(values[0]).replace('#', '')
        try:
            target_rank = int(rank_str)
            eval_rec = next((e for e in self.analyzer.evaluations if e.get('rank') == target_rank), None)
        except ValueError:
            eval_rec = None

        if not eval_rec:
            return

        CandidateDetailWindow(self.root, eval_rec, self.analyzer.jd_profile)

    def export_csv_summary(self):
        """Exports ranked candidate results to CSV file."""
        if not self.analyzer.evaluations:
            messagebox.showwarning("No Data", "Please run analysis before exporting CSV summary.")
            return

        default_filename = "resume_analysis_summary.csv"
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
        os.makedirs(out_dir, exist_ok=True)
        default_path = os.path.join(out_dir, default_filename)

        path = filedialog.asksaveasfilename(
            title="Save CSV Summary Export",
            initialdir=out_dir,
            initialfile=default_filename,
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if path:
            try:
                created_path = Exporter.export_to_csv(self.analyzer.evaluations, path)
                messagebox.showinfo("Export Successful", f"Successfully exported summary CSV to:\n{created_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Could not export CSV:\n{e}")

    def export_single_report(self):
        """Exports TXT report for selected candidate."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Candidate", "Please select a candidate to save TXT report.")
            return

        item = self.tree.item(selected[0])
        values = item['values']
        rank_str = str(values[0]).replace('#', '')
        try:
            target_rank = int(rank_str)
            eval_rec = next((e for e in self.analyzer.evaluations if e.get('rank') == target_rank), None)
        except ValueError:
            eval_rec = None

        if not eval_rec:
            return

        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "reports")
        try:
            report_path = Exporter.export_individual_txt_report(eval_rec, self.analyzer.jd_profile, out_dir)
            messagebox.showinfo("Report Saved", f"Saved candidate TXT report to:\n{report_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not save TXT report:\n{e}")

    def export_all_reports(self):
        """Exports TXT reports for all evaluated candidates."""
        if not self.analyzer.evaluations:
            messagebox.showwarning("No Data", "Please run analysis before exporting reports.")
            return

        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "reports")
        saved_paths = []
        try:
            for eval_rec in self.analyzer.evaluations:
                p = Exporter.export_individual_txt_report(eval_rec, self.analyzer.jd_profile, out_dir)
                saved_paths.append(p)
            messagebox.showinfo("Reports Saved", f"Successfully generated {len(saved_paths)} TXT candidate reports in folder:\n{out_dir}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not save all reports:\n{e}")

    def reset_all(self):
        """Resets application state, clearing JD, resumes, and dashboard table."""
        self.clear_jd()
        self.clear_resumes()
        self.analyzer = ResumeAnalyzer()

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.card_total.config(text="0")
        self.card_avg.config(text="0.0%")
        self.card_top.config(text="None")
        self.card_suitable.config(text="0")


class CandidateDetailWindow(tk.Toplevel):
    """Luxury Popup Modal Window showing comprehensive individual candidate analysis."""

    def __init__(self, parent: tk.Tk, eval_rec: Dict[str, Any], jd_profile: Dict[str, Any]):
        super().__init__(parent)
        self.title(f"Candidate Profile Analysis — {eval_rec['name']}")
        self.geometry("860x700")
        self.minsize(780, 600)
        self.configure(bg=LuxuryTheme.BG_DARK)
        self.transient(parent)
        self.grab_set()

        self.eval_rec = eval_rec
        self.cand = eval_rec['candidate_profile']
        self.score_info = eval_rec['score_info']
        self.jd = jd_profile

        self._build_ui()

    def _build_ui(self):
        """Builds candidate detailed profile layout."""
        # Top Header Card
        header_card = tk.Frame(self, bg=LuxuryTheme.CARD_BG, bd=1, relief="solid")
        header_card.pack(fill=tk.X, padx=16, pady=(16, 10))

        # Left Info Box
        info_box = tk.Frame(header_card, bg=LuxuryTheme.CARD_BG)
        info_box.pack(side=tk.LEFT, padx=16, pady=12)

        lbl_name = tk.Label(
            info_box,
            text=f"👤 {self.cand['name']}",
            font=(LuxuryTheme.FONT_FAMILY, 16, "bold"),
            fg=LuxuryTheme.TEXT_PRIMARY,
            bg=LuxuryTheme.CARD_BG
        )
        lbl_name.pack(anchor="w")

        lbl_contact = tk.Label(
            info_box,
            text=f"📧 {self.cand['email']}   |   📞 {self.cand['phone']}",
            font=LuxuryTheme.FONT_SUBTITLE,
            fg=LuxuryTheme.TEXT_MUTED,
            bg=LuxuryTheme.CARD_BG
        )
        lbl_contact.pack(anchor="w", pady=(4, 0))

        # Right Score Badge Box
        score_box = tk.Frame(header_card, bg=LuxuryTheme.CARD_BG)
        score_box.pack(side=tk.RIGHT, padx=16, pady=12)

        rec = self.eval_rec['recommendation']
        badge_bg, badge_fg = self._get_badge_colors(rec)

        rec_badge = tk.Label(
            score_box,
            text=f" {rec.upper()} ",
            font=LuxuryTheme.FONT_BOLD,
            fg=badge_fg,
            bg=badge_bg,
            padx=10,
            pady=4
        )
        rec_badge.pack(anchor="e")

        lbl_score = tk.Label(
            score_box,
            text=f"Score: {self.eval_rec['total_score']}%  (Rank #{self.eval_rec.get('rank', 1)})",
            font=LuxuryTheme.FONT_HEADER,
            fg=LuxuryTheme.GOLD_TEXT,
            bg=LuxuryTheme.CARD_BG
        )
        lbl_score.pack(anchor="e", pady=(4, 0))

        # Main Scrollable Content Box
        main_frame = tk.Frame(self, bg=LuxuryTheme.BG_DARK)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=6)

        # 1. Progress Bars Section Card
        prog_card = tk.LabelFrame(
            main_frame,
            text=" 📊 WEIGHTED COMPONENT BREAKDOWN ",
            font=LuxuryTheme.FONT_HEADER,
            fg=LuxuryTheme.GOLD_PRIMARY,
            bg=LuxuryTheme.CARD_BG,
            bd=1,
            relief="solid"
        )
        prog_card.pack(fill=tk.X, pady=(0, 10))

        self._create_component_progress(prog_card, "Skills Match (50% Weight)", self.score_info['skills_score'])
        self._create_component_progress(prog_card, "Experience (20% Weight)", self.score_info['experience_score'])
        self._create_component_progress(prog_card, "Education (15% Weight)", self.score_info['education_score'])
        self._create_component_progress(prog_card, "Keyword Relevance (15% Weight)", self.score_info['keyword_score'])

        # 2. Detailed Skills & Qualifications Grid
        grid_frame = tk.Frame(main_frame, bg=LuxuryTheme.BG_DARK)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        # Matched Skills Box
        matched_box = tk.LabelFrame(
            grid_frame,
            text=f" ✅ MATCHED SKILLS ({len(self.score_info['matched_skills'])}) ",
            font=LuxuryTheme.FONT_BOLD,
            fg=LuxuryTheme.COLOR_SUITABLE,
            bg=LuxuryTheme.CARD_BG,
            bd=1,
            relief="solid"
        )
        matched_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        matched_str = "\n".join([f"•  {s}" for s in self.score_info['matched_skills']]) if self.score_info['matched_skills'] else "None matched"
        lbl_matched = tk.Label(
            matched_box,
            text=matched_str,
            font=LuxuryTheme.FONT_BODY,
            fg=LuxuryTheme.TEXT_SECONDARY,
            bg=LuxuryTheme.CARD_BG,
            justify=tk.LEFT,
            anchor="nw",
            padx=10,
            pady=10
        )
        lbl_matched.pack(fill=tk.BOTH, expand=True)

        # Missing Skills Box
        missing_box = tk.LabelFrame(
            grid_frame,
            text=f" ❌ MISSING SKILLS ({len(self.score_info['missing_skills'])}) ",
            font=LuxuryTheme.FONT_BOLD,
            fg=LuxuryTheme.COLOR_UNSUITABLE,
            bg=LuxuryTheme.CARD_BG,
            bd=1,
            relief="solid"
        )
        missing_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        missing_str = "\n".join([f"•  {s}" for s in self.score_info['missing_skills']]) if self.score_info['missing_skills'] else "None! All required skills present."
        lbl_missing = tk.Label(
            missing_box,
            text=missing_str,
            font=LuxuryTheme.FONT_BODY,
            fg=LuxuryTheme.TEXT_SECONDARY,
            bg=LuxuryTheme.CARD_BG,
            justify=tk.LEFT,
            anchor="nw",
            padx=10,
            pady=10
        )
        lbl_missing.pack(fill=tk.BOTH, expand=True)

        # 3. Dynamic Executive Assessment Card
        assess_card = tk.LabelFrame(
            main_frame,
            text=" 💡 DYNAMIC EXECUTIVE ASSESSMENT ",
            font=LuxuryTheme.FONT_HEADER,
            fg=LuxuryTheme.GOLD_PRIMARY,
            bg=LuxuryTheme.CARD_BG,
            bd=1,
            relief="solid"
        )
        assess_card.pack(fill=tk.X, pady=(10, 0))

        lbl_assess = tk.Label(
            assess_card,
            text=f'"{self.eval_rec["assessment_summary"]}"',
            font=(LuxuryTheme.FONT_FAMILY, 10, "italic"),
            fg=LuxuryTheme.TEXT_PRIMARY,
            bg=LuxuryTheme.CARD_BG,
            wraplength=780,
            justify=tk.LEFT,
            padx=12,
            pady=12
        )
        lbl_assess.pack(fill=tk.X)

        # Bottom Close Button
        btn_close = tk.Button(
            self,
            text="Close Window",
            font=LuxuryTheme.FONT_BOLD,
            fg=LuxuryTheme.TEXT_PRIMARY,
            bg="#252525",
            activebackground="#333333",
            bd=0,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.destroy
        )
        btn_close.pack(pady=12)

    def _create_component_progress(self, parent: tk.Frame, label: str, val: float):
        """Builds custom progress indicator row."""
        row = tk.Frame(parent, bg=LuxuryTheme.CARD_BG)
        row.pack(fill=tk.X, padx=12, pady=4)

        lbl = tk.Label(row, text=label, font=LuxuryTheme.FONT_BODY, fg=LuxuryTheme.TEXT_SECONDARY, bg=LuxuryTheme.CARD_BG, width=28, anchor="w")
        lbl.pack(side=tk.LEFT)

        pbar = ttk.Progressbar(row, style="Gold.Horizontal.TProgressbar", length=360, maximum=100, value=val)
        pbar.pack(side=tk.LEFT, padx=10)

        val_lbl = tk.Label(row, text=f"{val}%", font=LuxuryTheme.FONT_BOLD, fg=LuxuryTheme.GOLD_TEXT, bg=LuxuryTheme.CARD_BG, width=8, anchor="e")
        val_lbl.pack(side=tk.LEFT)

    def _get_badge_colors(self, rec: str) -> tuple:
        """Returns background and foreground colors for recommendation badge."""
        if rec == "Highly Suitable":
            return LuxuryTheme.BG_HIGHLY_SUITABLE, LuxuryTheme.COLOR_HIGHLY_SUITABLE
        elif rec == "Suitable":
            return LuxuryTheme.BG_SUITABLE, LuxuryTheme.COLOR_SUITABLE
        elif rec == "Potential Candidate":
            return LuxuryTheme.BG_POTENTIAL, LuxuryTheme.COLOR_POTENTIAL
        elif rec == "Partially Suitable":
            return LuxuryTheme.BG_PARTIAL, LuxuryTheme.COLOR_PARTIAL
        else:
            return LuxuryTheme.BG_UNSUITABLE, LuxuryTheme.COLOR_UNSUITABLE
