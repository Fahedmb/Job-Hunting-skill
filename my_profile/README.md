# Candidate Profile Setup & Onboarding Guide

Welcome to **Agentic Job Hunter**! Your profile is the **Single Source of Truth** that your AI agent relies upon to tailor your CV, motivation letters, and emails.

---

## 3 Quick Ways to Onboard Your Information

### 🚀 Option 1: The Automated AI Ingestion (Fastest)
1. Drop your existing PDF or DOCX resume(s) into the `my_profile/old_cv/` folder.
2. Open your AI agent of choice (Antigravity, Claude Code, Cursor, Windsurf, or ChatGPT) and send this prompt:
   > *"Please read my existing CV from `my_profile/old_cv/` and create my `my_profile/candidate_profile.md` using the structure in `my_profile/candidate_profile.example.md`. Transform my experience bullets into Action-Scale-Outcome (ASO) format and extract all my verified skills."*
3. The agent will read your PDF, extract your background, and generate your clean `candidate_profile.md`. Review and adjust if desired!

### ✍️ Option 2: Copy the Example Template
1. Duplicate `candidate_profile.example.md` and name the new file `candidate_profile.md`:
   ```bash
   cp my_profile/candidate_profile.example.md my_profile/candidate_profile.md
   ```
2. Open `my_profile/candidate_profile.md` in your editor and replace the placeholder data with your real information.

### 💬 Option 3: Interactive Prompt Onboarding
If you don't have a PDF handy:
1. Paste your LinkedIn text, bio, or informal work history directly into the agent chat:
   > *"Here is my work history and education. Please create my `my_profile/candidate_profile.md` following the template in `my_profile/candidate_profile.example.md`."*
2. The agent will parse and structure it for you.

---

## ⚠️ The Golden Rule: Zero-Fabrication (Truth Engine)

The core philosophy of this project is **authentic alignment**:
- The AI agent will **never invent, fabricate, or hallucinate** tools, degrees, or years of experience.
- When applying for jobs, the agent selects, prioritizes, and reorders your **real, verified skills and achievements** that best match the employer's requirements.
- If a job description asks for tools you do not know, the agent highlights your strong foundational background honestly, rather than falsely claiming unverified tools.

---

## 🔒 Privacy Notice
Your `candidate_profile.md`, `email_config.json` (mailbox app password), and any PDFs inside `old_cv/` are **automatically ignored by `.gitignore`**. Your personal contact information, phone numbers, addresses, and email credentials will **never** be committed to your public Git repository. Only `email_config.example.json` (the empty template) is shared.
