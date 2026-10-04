<div align="center">

# 🎯 Job-Hunting-skill
### The Open-Source Multi-Agent Career Engineering Platform

**Turn any AI agent into your personal, autonomous career co-pilot.**  
Conduct deep company intelligence, analyze fit, generate ATS-optimized 1-page LaTeX CVs, matching cover letters, phone-screen cheat sheets, and high-converting outreach pitches — grounded 100% in your authentic background.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Multi-Agent: Antigravity | Claude | Cursor | Windsurf](https://img.shields.io/badge/Agents-Antigravity%20%7C%20Claude%20%7C%20Cursor%20%7C%20Windsurf-7928CA.svg)](#-agent-compatibility)
[![LaTeX: Zero--Error 1--Page](https://img.shields.io/badge/LaTeX-Strict%201--Page%20Budget-007acc.svg)](#-latex-architecture--compilation)
[![ATS: Hybrid Search Optimized](https://img.shields.io/badge/ATS-Hybrid%20%26%20Neural%20Search%20Ready-success.svg)](docs/ats_optimization_guide.md)

</div>

---

## ⚡ What Makes This Different?

Most AI resume builders create generic, uninspired summaries and hallucinate skills that get you rejected in the first interview. **Job-Hunting-skill** is built on four non-negotiable engineering principles:

1. **🛡️ The Zero-Fabrication Rule (Truth Engine):**  
   Your candidate profile (`my_profile/candidate_profile.md`) is the **immutable single source of truth**. The agent is strictly forbidden from inventing fake tools or credentials. Tailoring means selecting, prioritizing, and framing your *real, verified achievements* to highlight maximum relevance for the target role.

2. **📊 Action-Scale-Outcome (ASO) Bullet Engineering:**  
   Every single bullet point is formulated as:  
   $$\textbf{[Strong Active Verb]} + \textbf{[Domain/Tech Scope \& Scale]} + \textbf{[Quantified Business Outcome]}$$  
   Engineered for the recruiter's **6-second scan** and modern neural ATS embeddings.

3. **📄 Strict Single-Page LaTeX Architecture:**  
   Beautiful, single-column, machine-readable LaTeX templates with Bitstream Charter typography and subtle NavyBlue accents. Guaranteed to fit on **exactly 1 page** without awkward page breaks or clipped margins.

4. **🤖 100% Agent-Agnostic & Zero Vendor Lock-in:**  
   Works natively with **Google Antigravity**, **Claude Code**, **Cursor**, **Windsurf**, **GitHub Copilot**, or standard web LLMs (**ChatGPT**, **Claude.ai**, **Gemini**).

---

## 🏗️ Architecture & Workflow

```
[ User provides Job URL or Job Description ]
                     │
                     ▼
[ Step 1: Deep Company Intelligence & Web Research ]
  ├─► Business model, core products, target audience
  ├─► Tech stack, engineering culture, and recent news
  └─► Fit & Gap Analysis against your verified profile
                     │
                     ▼
[ Step 2: Dedicated Application Workspace ]
  └─► Created under applications/<Company> - <Role>/
                     │
                     ▼
[ Step 3: 30-Second Recruiter Phone Screen Cheat Sheet ]
  └─► Saved in job_offer.md (elevator pitch, talking points, salary script)
                     │
                     ▼
[ Step 4: Tailored 1-Page ATS CV (LaTeX -> PDF) ]
  └─► CV_<Name>.pdf (Strictly 1 page, no company name in file name)
                     │
                     ▼
[ Step 5: Matching 1-Page Motivation Letter (LaTeX -> PDF) ]
  └─► Cover_Letter_<Name>.pdf ("Vous / Moi / Nous" framework)
                     │
                     ▼
[ Step 6: Multi-Channel Outreach Suite ]
  ├─► Formal HR / Portal Application Email
  ├─► Direct Pitch to Founder / CTO / Hiring Manager
  └─► Short LinkedIn Connection Note (< 300 chars)
                      │
                      ▼
[ Step 6b: Email Draft in Your Mailbox (only on your YES) ]
  └─► Draft via IMAP or .eml file, CV + letter attached, never auto-sent
                      │
                      ▼
[ Step 7: Central Application Tracker ]
  └─► Automatically appended to applications/applications_tracker.md
```

---

## 🚀 Quickstart Guide (3 Simple Steps)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Fahedmb/Job-Hunting-skill.git
cd Job-Hunting-skill
```

### Step 2: Onboard Your Profile (Pick One)

* **Method A (Automated from Old CV):**  
  Drop your existing resume (`resume.pdf` or `.docx`) into `my_profile/old_cv/`.  
  Tell your agent:  
  > *"Please extract my background from `my_profile/old_cv/` and populate `my_profile/candidate_profile.md` using the template."*
* **Method B (Copy & Edit Template):**  
  ```bash
  cp my_profile/candidate_profile.example.md my_profile/candidate_profile.md
  ```
  Edit `candidate_profile.md` with your verified roles, projects, and skills.
* **Method C (Prompt-Driven):**  
  Paste your LinkedIn profile text or career history into the agent chat and ask it to scaffold your profile.

### Step 3: Apply to Any Job
Paste a job posting into your agent chat:
> *"Here is a job offer from [Company Name] for a [Role Title] position: [Paste URL or text].  
> Research the company, analyze my fit, create the application folder, tailor my 1-page CV and Cover Letter, compile to PDF, and draft outreach emails."*

---

## 🛠️ LaTeX Compilation & Local Engine Setup

The platform includes automated tools to detect, install, and compile your LaTeX documents into zero-error PDFs:

```bash
# Check if LaTeX is installed (or auto-install if supported)
python tools/setup_latex.py --auto-install

# Compile a CV or cover letter and verify the strict 1-page budget
python tools/compile_latex.py "applications/Acme - Senior Engineer/CV_Alex_Rivera.tex"
```

### Supported LaTeX Compilers
- **Windows:** `pdflatex` (MiKTeX) or `tectonic` (`winget install Tectonic.Tectonic`)
- **macOS:** `brew install --cask mactex-no-gui` or `brew install tectonic`
- **Linux (Ubuntu/Debian):** `sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra` or `sudo apt-get install -y tectonic`
- **Docker:** `docker run --rm -v "${PWD}:/data" dxjoke/tectonic tectonic document.tex`

### 🌐 No Local LaTeX? No Problem!
If your corporate device or environment restricts installing software:
1. The agent generates a clean, zero-error `.tex` file.
2. Go to **[Overleaf.com](https://www.overleaf.com/)** (Free).
3. Paste the `.tex` code into a Blank Project and click **Recompile** to download your PDF instantly.

---

## 🤖 Agent Compatibility

| Platform | Native Configuration File | Instructions |
| :--- | :--- | :--- |
| **Google Antigravity** | [`skills/job-hunter/SKILL.md`](skills/job-hunter/SKILL.md) | Loaded automatically in workspace, or copy to `~/.gemini/config/skills/` |
| **Claude Code** | [`CLAUDE.md`](CLAUDE.md) | Loaded natively when running `claude` in repo root |
| **OpenCode** | [`OPENCODE.md`](OPENCODE.md) | Loaded natively when running `opencode` in repo root |
| **Cursor IDE** | [`.cursorrules`](.cursorrules) & [`.cursor/rules/`](.cursor/rules/job-tailor.mdc) | Loaded automatically in Cursor Composer & Chat (`Ctrl+L`) |
| **Windsurf (Cascade)** | [`.windsurfrules`](.windsurfrules) | Loaded automatically by Cascade (`Ctrl+I`) |
| **GitHub Copilot / Open Agents** | [`AGENTS.md`](AGENTS.md) | Standard cross-agent specification |
| **ChatGPT / Claude.ai Web** | [`SYSTEM_PROMPT.md`](SYSTEM_PROMPT.md) | Copy-paste system prompt into custom instructions or web chat |

---

## 📂 Repository Structure

```
Job-Hunting-skill/
├── .cursorrules                       # Cursor IDE configuration
├── .cursor/rules/job-tailor.mdc       # Cursor MDC rules engine
├── .windsurfrules                     # Windsurf / Cascade configuration
├── CLAUDE.md                          # Claude Code native instructions
├── OPENCODE.md                         # OpenCode native instructions
├── AGENTS.md                          # Cross-agent specification standard
├── SYSTEM_PROMPT.md                   # Standalone prompt for ChatGPT / Claude Web
├── configuration4Draft.md             # Email draft setup guide (IMAP + .eml fallback)
├── README.md                          # Documentation & quickstart
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Community guidelines
├── .gitignore                         # Protects candidate profile & personal applications
├── my_profile/                        # Candidate Single Source of Truth
│   ├── candidate_profile.example.md   # Universal template for any industry
│   ├── email_config.example.json      # Email draft settings template (copy to email_config.json, never committed)
│   ├── README.md                      # Onboarding guide (PDF drop vs prompt)
│   └── old_cv/                        # Place old PDF/DOCX resumes here
│       └── .gitkeep
├── templates/
│   ├── cv_template_en.tex             # Parameterized English 1-page ATS CV
│   ├── cv_template_fr.tex             # Parameterized French 1-page ATS CV
│   ├── cover_letter_template_en.tex   # Parameterized English 1-page Cover Letter
│   └── cover_letter_template_fr.tex   # Parameterized French 1-page Cover Letter
├── skills/
│   └── job-hunter/
│       └── SKILL.md                   # Google Antigravity / Gemini Agent Skill
├── docs/
│   ├── ats_optimization_guide.md      # ATS algorithms, Boolean logic, ASO formula
│   ├── cross_regional_recruitment.md  # EU vs US vs GCC vs Nearshore strategies
│   └── agent_setup_guide.md           # Multi-agent setup walkthroughs
├── tools/
│   ├── setup_latex.py                 # Detects & auto-installs LaTeX compilers
│   ├── compile_latex.py               # Auto-compiler with strict 1-page verification
│   ├── create_email_draft.py          # Creates mailbox drafts via IMAP (.eml fallback), gated by user YES
│   └── extract_profile.py             # Extracts text from PDF resumes
└── applications/                      # Your generated job applications
    ├── .gitkeep
    └── applications_tracker.md        # Central tracker table for all applications
```

---

## 🔒 Privacy & Data Protection

Your private career data is protected by design:
- `.gitignore` automatically excludes `my_profile/candidate_profile.md`, `my_profile/email_config.json`, `my_profile/old_cv/*`, and all individual folders inside `applications/`.
- You can freely commit and push improvements to your fork without leaking your contact details, target salaries, or application letters.

---

## 🤝 Contributing

Contributions are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) to add new LaTeX templates, translations, or agent adapters.

---

## 📄 License

Distributed under the [MIT License](LICENSE). Built with ❤️ by [Fahed Mbarek](https://github.com/Fahedmb) and the Open Source Career Engineering Community.
