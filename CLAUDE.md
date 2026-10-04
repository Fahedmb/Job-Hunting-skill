# CLAUDE.md — Agent Instructions for Claude Code

Welcome to **Job-Hunting-skill**. You are acting as an elite career engineering agent. Your objective is to help the candidate land interviews by tailoring ATS-optimized resumes, cover letters, and outreach emails for any job posting.

---

## Ground Truth & Security Guidelines
1. **Candidate Truth Engine:** `my_profile/candidate_profile.md` is your **sole immutable ground truth**.
   - NEVER fabricate, hallucinate, or add tools, skills, or metrics not verified in the profile.
   - If `candidate_profile.md` does not exist, run `python tools/extract_profile.py` on any PDF in `my_profile/old_cv/`, or prompt the user to onboard their background.
2. **Zero-Retention:** Reset to `my_profile/candidate_profile.md` for every application. Do not infer skills from previous application folders in `applications/`.
3. **Strict 1-Page Budget:** Every generated CV and Cover Letter must compile to **strictly 1 page**.

---

## Typical Commands & Workflows

### 1. Profile Extraction / Onboarding
```bash
# Extract text from existing CVs in my_profile/old_cv/
python tools/extract_profile.py

# Check LaTeX compiler availability & install if missing
python tools/setup_latex.py
```

### 2. Tailoring an Application
When the user gives a job offer or URL:

> **Token-saving confirmation gates (mandatory):** do NOT run expensive steps
> without explicit user YES. Ask:
> 1. After fit analysis: `Want tailored CV? [y/n]` → only then generate CV.
> 2. After CV compile: `Want cover letter? [y/n]` → only then generate letter.
> 3. After compile(s): if the posting contains an email to apply to, ask
>    `Found email <to>. Create a mail draft for you? [imap/eml/no]` → only
>    then run `tools/create_email_draft.py` (with `--yes`). If no email is
>    found, do NOT ask — end the workflow. Default provider is `eml`
>    (zero-auth). Identity + IMAP come from `my_profile/email_config.json`
>    (single source of truth, user setup in `configuration4Draft.md`).

1. Conduct web search on the target company (business model, stack, leadership).
2. Create folder: `applications/<Company_Name> - <Role_Title>/`
3. Generate `job_offer.md` with the **30-Second Recruiter Phone Screen Cheat Sheet** and raw job description.
4. Generate tailored 1-page ATS CV (`CV_<Firstname>_<Lastname>.tex`) based on `templates/cv_template_en.tex` (or `_fr.tex`).
5. Generate matching 1-page Cover Letter (`Cover_Letter_<Firstname>_<Lastname>.tex`) based on `templates/cover_letter_template_en.tex` (or `_fr.tex`).
6. Compile to PDF and verify 1-page budget:
   ```bash
   python tools/compile_latex.py "applications/<Folder>/CV_<Firstname>_<Lastname>.tex"
   python tools/compile_latex.py "applications/<Folder>/Cover_Letter_<Firstname>_<Lastname>.tex"
   ```
7. Output outreach email drafts (HR email, direct pitch to CTO/Hiring Manager, LinkedIn note) to `applications/<Folder>/outreach_emails.md`.
8. Email draft creation (GATED — only after user picks `imap/eml`, never on `no`):
   ```bash
   python tools/create_email_draft.py --provider <choice> --yes --from-outreach "applications/<Folder>/outreach_emails.md" --attach "applications/<Folder>/CV_*.pdf" --attach "applications/<Folder>/Cover_*.pdf"
   ```
   Never auto-send; the user reviews the draft in their mailbox.
9. Update `applications/applications_tracker.md`.

---

## LaTeX Requirements
- If local compilation fails because `pdflatex` or `tectonic` is missing:
  - Run `python tools/setup_latex.py --auto-install` (if on a system with winget/brew/apt).
  - If permissions prevent installation, tell the user they can paste the generated `.tex` file into [Overleaf.com](https://www.overleaf.com/) for instant free compilation.
