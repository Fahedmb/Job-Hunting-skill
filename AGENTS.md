# AGENTS.md — Universal Agent Instructions for Job-Hunting-skill

This file defines the project instructions, architectural boundaries, and operational workflows for autonomous AI coding agents (GitHub Copilot, Codex, Windsurf, Cursor, Claude Code, Antigravity, OpenHands, Cline).

---

## 1. Project Overview & Philosophy
**Job-Hunting-skill** is an open-source, multi-agent career engineering platform. It transforms raw candidate experience into high-conversion, ATS-optimized, 1-page LaTeX CVs, matching cover letters, company intelligence dossiers, and multi-channel outreach pitches for any target role.

### The Immutable Ground Truth Rule
- `my_profile/candidate_profile.md` is the **sole source of truth**.
- Agents must **NEVER** hallucinate or claim unverified skills or tools.
- Tailoring is the strategic selection and prioritization of authentic candidate evidence.

---

## 2. Onboarding Workflow
If `my_profile/candidate_profile.md` is missing:
1. Look for existing resume files in `my_profile/old_cv/`.
2. Extract text using `python tools/extract_profile.py` or native file reading.
3. Structure the extracted details into `my_profile/candidate_profile.md` following `my_profile/candidate_profile.example.md`.
4. Ensure experience bullets are converted into the **Action-Scale-Outcome (ASO)** format:
   $$\text{Bullet} = \textbf{[Active Verb]} + \textbf{[Scope/Tech Context]} + \textbf{[Quantified Business Outcome]}$$

---

## 3. Job Application Pipeline
When presented with a job description or URL:

> **Token-saving confirmation gates (mandatory):** do NOT run expensive steps
> without explicit user YES. Ask:
> 1. After fit analysis: `Want tailored CV? [y/n]` → only then generate CV.
> 2. After CV compile: `Want cover letter? [y/n]` → only then generate letter.
> 3. After compile(s): if the job description contains a mailing list to apply to, ask Found email <to>. Create a mail draft for you? [imap/eml/no]
   >→ only then run tools/create_email_draft.py (with --yes).
   >If no mailing list is found, do NOT ask — end the workflow.
   >Default provider is eml (zero-auth). See configuration4Draft.md for
   >generic IMAP one-time setup (works for Gmail/Outlook/Yahoo/iCloud).
1. **Company Web Intelligence:**
   - Search the web for company details: core business, products, stack/domain, engineering culture, and key leadership.
2. **Directory Setup:**
   - Create `applications/<Company_Name> - <Role_Title>/`.
3. **`job_offer.md` Generation:**
   - Compile the **30-Second Recruiter Phone Screen Cheat Sheet** (key pitch points, company overview, target salary script).
   - Preserve raw job posting verbatim.
4. **1-Page ATS CV Generation:**
   - Use `templates/cv_template_en.tex` (or `_fr.tex`).
   - Output to `applications/<Company> - <Role>/CV_<Firstname>_<Lastname>.tex`.
   - Ensure strictly 1 page.
5. **1-Page Cover Letter Generation:**
   - Use `templates/cover_letter_template_en.tex` (or `_fr.tex`).
   - Use the **Vous / Moi / Nous** structure.
   - Output to `applications/<Company> - <Role>/Cover_Letter_<Firstname>_<Lastname>.tex`.
6. **PDF Compilation & Single-Page Verification:**
   - Run `python tools/compile_latex.py "<path_to_tex>"`.
   - If LaTeX is missing, execute `python tools/setup_latex.py --auto-install`.
   - If local installation is restricted by the platform, inform the user they can paste the `.tex` into [Overleaf.com](https://www.overleaf.com/).
7. **Outreach Email Generation:**
   - Variant A: Formal HR / application email.
   - Variant B: Direct pitch to Hiring Manager / Founder / CTO.
   - Variant C: LinkedIn InMail / connection note (< 300 chars).
   - Save to `applications/<Company> - <Role>/outreach_emails.md`.
8. **Email Draft Creation (GATED):**
   - Only after user picks `imap/eml` (never on `no`).
   - Identity + IMAP come from `my_profile/email_config.json` (single source of truth, user setup in `configuration4Draft.md`).
   - Run `python tools/create_email_draft.py --provider <choice> --yes --from-outreach "<folder>/outreach_emails.md" --attach <CV.pdf> --attach <Cover.pdf>`.
   - Never auto-send; user reviews the draft in their mailbox.
9. **Tracker Update:**
   - Log entry in `applications/applications_tracker.md`.
