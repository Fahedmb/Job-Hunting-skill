---
name: "job-hunting-tailor"
description: "Universal automated end-to-end job application tailor and career engineering skill. When provided a job description or URL, this skill conducts deep web intelligence on the company, analyzes fit against the candidate's verified profile, generates ATS-optimized 1-page CV and matching 1-page Motivation Letter in LaTeX (without company name in the file name), verifies zero-error compilation with local LaTeX tools, drafts multi-channel application emails, and maintains an applications tracker."
category: "career-engineering"
risk: "safe"
source: "custom"
author: "Open Source Career Engineering Community"
tags: ["resume", "cv", "latex", "cover-letter", "ats-optimization", "job-hunting", "web-research", "multi-agent", "recruitment", "semantic-search"]
tools: ["run_command", "view_file", "write_to_file", "replace_file_content", "search_web", "read_url_content"]
---

# Universal Job Application Tailor & Career Engineering Skill

This skill automates the complete job application pipeline for **any candidate across any professional field** (Software Engineering, Data Science, Product, Marketing, Finance, Industrial Engineering, Healthcare, etc.).

It is engineered to maximize match scores across modern **Applicant Tracking Systems (ATS)**, neural semantic retrieval engines (LLM embeddings / Cosine Similarity), and human technical hiring managers.

---

## 1. Candidate Truth Engine (Single Source of Truth)

### ⚠️ STRICT CORE RULES: ZERO-FABRICATION & COMPLETE PROFILE ISOLATION
1. **The Candidate Profile (`my_profile/candidate_profile.md`) is the SOLE IMMUTABLE GROUND TRUTH.**
   - If `my_profile/candidate_profile.md` does not yet exist:
     - Check `my_profile/old_cv/` for existing resumes and run `tools/extract_profile.py` or inspect the files with `view_file` to scaffold `candidate_profile.md`.
     - Or prompt the user for their background details and generate `my_profile/candidate_profile.md` before tailoring.
2. **ZERO-FABRICATION / NO FAKE SKILLS:**
   - **NEVER** fabricate, invent, or add skills, tools, frameworks, metrics, or credentials not present in the candidate profile.
   - Strictly FORBIDDEN to claim proficiency in unverified tools just because a job posting asks for them.
3. **ZERO-RETENTION / COMPLETE APPLICATION ISOLATION:**
   - **NEVER** read from or reference previous application folders (e.g. `applications/Company XYZ/`) to infer candidate skills.
   - For every new application, **ALWAYS** reset directly to `my_profile/candidate_profile.md`. Never carry over keywords hallucinated in prior runs.
4. **AUTHENTIC TAILORING DEFINITION:**
   - Tailoring means selecting, prioritizing, and re-ordering the **real, verified skills, achievements, and experiences** from `candidate_profile.md` that best align with the target role.
   - The skills block in any tailored CV MUST be a STRICT SUBSET of the candidate's actual profile.
   - If a job description requires technologies or skills the candidate does not have, be 100% honest: highlight their verified adjacent strengths and fast ramp-up capabilities without claiming false mastery.

---

## 2. ATS & Recruiter Document Engineering Standards

Modern ATS platforms (Workday, Greenhouse, Personio, Textkernel, Bayt, Keejob) use **hybrid retrieval**: Boolean filters isolate the candidate pool, while vector embeddings score contextual proximity.

### A. Document Ingestion Integrity
- **Strict Single-Column Flow:** Linear top-to-bottom and left-to-right text stream. Never use multi-column tables, sidebars, floating text frames, or graphical rating bars.
- **Body Stream Header:** Contact details (Name, Location, Phone, Email, Links) **must live in the primary document body**. Never put contact info in `\fancyhead` or `\fancyfoot` macros (parsers discard them).
- **Machine-Readable Unicode:** Always compile with `\pdfgentounicode=1`, `\usepackage{cmap}`, and `\usepackage[T1]{fontenc}` in LaTeX.
- **Recognized Section Headings:** Use standard section names (`Professional Summary`, `Technical Skills` / `Core Competencies`, `Professional Experience`, `Key Projects`, `Education`).

### B. Action-Scale-Outcome (ASO) Bullet Formula
Every bullet point in Experience and Projects must follow the **Action-Scale-Outcome (ASO)** formula:

$$\text{Bullet} = \textbf{[Strong Active Verb]} + \textbf{[Domain/Technical Stack \& Scale Context]} + \textbf{[Quantified Outcome / Business Value]}$$

- **Active Verbs:** *Architected, Engineered, Implemented, Designed, Streamlined, Spearheaded, Automated, Optimized, Deployed*.
- **Scale:** Quantitative scope (*5 microservices, 15M+ daily requests, $2M pipeline, 120k active users, 15+ client platforms*).
- **Outcome:** Measurable impact (*reduced latency by 42%, cut manual processing time by >40%, achieved 99.98% uptime, boosted conversion by 18%*).

---

## 3. End-to-End Application Workflow

Whenever a user provides a job description or URL, execute these steps systematically.

> **Token-saving rule (confirmation gates):** generating a CV (~2-4k tokens),
> cover letter (~1-2k), and web research (~3k) is expensive. After each cheap
> step, STOP and ask for explicit YES/NO before continuing:
> 1. After fit analysis: `Want tailored CV? [y/n]`
> 2. After CV compile: `Want cover letter? [y/n]`
> 3. After compile(s): `Found email <to>. Create a mail draft for you? [imap/eml/no]`
> Never run a gated step without explicit user confirmation. Default to the
> cheapest path (`.eml`, no credentials) unless the user picks imap.
> Setup details: see `configuration4Draft.md`.

### Step 0: Verify Candidate Profile
Confirm `my_profile/candidate_profile.md` exists. If not, guide the user to drop their CV in `my_profile/old_cv/` or provide their details, then generate it.

### Step 1: Company Web Research & Intelligence
1. **Targeted Web Search (`search_web` / `read_url_content`):**
   - Conduct targeted search on the hiring company:
     - Core products, platforms, business model, and target customers.
     - Tech stack, engineering/work culture, public open-source repos, or technological initiatives.
     - Key news, recent funding/acquisitions, or key leadership (Founders, CTO, Head of Talent).
2. **Fit & Gap Analysis:**
   - Calculate match percentage (e.g. 85% – 95%).
   - Map candidate's real project evidence to stated requirements.
   - Note genuine gaps and plan how to address them honestly.

### Step 2: Create Dedicated Application Folder & `job_offer.md`
1. Create a clean directory under `applications/`:
   ```bash
   applications/<Company_Name> - <Role_Title>/
   ```
2. Create `job_offer.md` inside that folder containing:
   - **Metadata Header:** Company, Role, Location, Date, Target Salary / Market benchmarks.
   - **⚡ 30-Second Recruiter Phone Screen Cheat Sheet:**
     - **Who They Are & What They Do:** 2-3 bullets on their business, product, and market.
     - **Key Decision Makers:** Names and roles found during web research.
     - **Top 3 Stories / Projects to Pitch:** Concrete proof points aligned with the role.
     - **Salary Range Script:** Pre-calculated, market-accurate verbal response.
     - **Availability & Languages:** Notice period, work authorization, language levels.
   - **📄 Full Raw Job Posting:** Complete, unedited text of the job description preserved verbatim.

### Step 3: Generate the Tailored 1-Page ATS CV
1. Choose the language: English (`templates/cv_template_en.tex`) or French (`templates/cv_template_fr.tex`).
2. Populate the template with the candidate's real data tailored to the role.
3. **File Name Rule:** Must **NOT** contain the company name in the file name itself (e.g. `CV_<Firstname>_<Lastname>.tex` $\rightarrow$ `CV_<Firstname>_<Lastname>.pdf`).
4. **Skills Policy:** Must be a strict subset of the candidate's verified skills.
5. **Length Budget:** Must fit on **EXACTLY 1 PAGE**.

### Step 4: Generate the Matching 1-Page Motivation Letter
1. Choose the language: English (`templates/cover_letter_template_en.tex`) or French (`templates/cover_letter_template_fr.tex`).
2. Structure follows the **Vous / Moi / Nous** (Company / Candidate / Shared Value) formula:
   - **Vous (The Company):** Specific opening referencing their actual mission, tech challenges, or market position from web research.
   - **Moi (The Candidate):** Honest alignment of candidate's verified background and quantified ASO achievements.
   - **Nous (The Impact):** How the candidate brings immediate productivity and rigor to their specific goals.
3. **File Name Rule:** `Cover_Letter_<Firstname>_<Lastname>.tex` $\rightarrow$ `Cover_Letter_<Firstname>_<Lastname>.pdf` (or `Lettre_Motivation_<Firstname>_<Lastname>.tex`).
4. **Length Budget:** Exactly 1 page (or concise < 250 words when requested).

### Step 5: Compile with LaTeX & Verify 1-Page Budget
1. Check if a local LaTeX compiler (`pdflatex`, `tectonic`, `xelatex`) is installed.
   - You can run `python tools/compile_latex.py "<path_to_tex_file>"`.
2. **If LaTeX compiler is available:**
   - Compile `.tex` to `.pdf`.
   - Remove auxiliary files (`.aux`, `.log`, `.out`).
   - Validate that the output PDF is **exactly 1 page**.
3. **If LaTeX compiler is NOT installed:**
   - Attempt automated installation via `python tools/setup_latex.py --auto-install` if platform allows it.
   - If the platform does not allow CLI installations (e.g., restricted web sandbox), explain to the user:
     > *"No local LaTeX compiler is installed. You can compile your zero-error `.tex` file in 5 seconds for free at [Overleaf.com](https://www.overleaf.com/) or install LaTeX locally with `python tools/setup_latex.py`."*

### Step 6: Multi-Channel Outreach Suite
Draft a ready-to-send application package in the chat:
- **Variant A (Official HR / Portal Application):** Formal email with structured value proposition and resume attachment mention.
- **Variant B (Direct Decision Maker Pitch):** Direct, punchy message to the Founder, CTO, or Hiring Manager.
- **Variant C (Short LinkedIn Note):** Concise connection message (< 300 characters or < 150 words).
- Save all three variants to `applications/<Company> - <Role>/outreach_emails.md`.

### Step 6b: Email Draft Creation (GATED — user confirmation required)
Only after the user answers YES to
`Found email <to>. Create a mail draft for you? [imap/eml/no]`:
(Single source of truth: `my_profile/email_config.json` holds sender
identity + IMAP connection — user setup is in `configuration4Draft.md`.
Content comes from the application folder, never from flags.)
1. **`imap` (cloud draft, any provider):** only if `email_config.json` is
   complete, run
   `python tools/create_email_draft.py --provider imap --yes --from-outreach "<folder>/outreach_emails.md" --attach "<folder>/CV_*.pdf" --attach "<folder>/Cover_*.pdf"`.
   On failure, the script falls back to `.eml` automatically.
2. **Default (`eml`, zero-auth):** run with `--provider eml`
   → produces `<folder>/Draft_Email.eml` (always works, no credentials).
3. **Never auto-send.** The tool only creates drafts (`--yes` flag is the
   explicit-consent gate; the script refuses without it). User reviews the
   draft in their mailbox before sending.

### Step 7: Update Central Applications Tracker
Append an entry to `applications/applications_tracker.md`:
```markdown
| Date | Company | Role Title | Location & Work Model | Key Contacts | Target Salary | Status | Folder Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
```
