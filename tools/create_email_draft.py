#!/usr/bin/env python3
"""
create_email_draft.py — Email Draft Creator (Generic IMAP + EML fallback)

Creates a ready-to-send application email draft AFTER the CV and Cover Letter
PDFs are compiled, and ONLY after explicit user confirmation.

Single source of truth: my_profile/email_config.json
  Holds sender identity + IMAP connection (works for ALL mailboxes —
  Gmail, Outlook, Yahoo, iCloud, custom domains). Copy the template once:
    cp my_profile/email_config.example.json my_profile/email_config.json
  then fill in your address + IMAP app password (file is gitignored).

Per-application content (recipient / subject / body / PDFs) always comes
from the application folder — never from the config:
  --from-outreach points at outreach_emails.md (Variant A is extracted),
  --attach adds the compiled PDFs (or all *.pdf in that folder by default).

Providers:
  1. imap (cloud draft): APPENDs to the Drafts folder via stdlib imaplib.
  2. eml  (fallback, zero-auth): builds Draft_Email.eml next to the outreach
     file; opens as a draft in Outlook / Apple Mail / Thunderbird.

Usage (agent MUST ask user first, see SKILL.md checkpoints):

  python tools/create_email_draft.py --provider imap --yes \
    --from-outreach "applications/Acme - Java/outreach_emails.md" \
    --attach "applications/Acme - Java/CV_Firstname_Lastname.pdf" \
    --attach "applications/Acme - Java/Cover_Letter_Firstname_Lastname.pdf"

Security:
  - NEVER auto-send. This tool only creates DRAFTS.
  - NEVER commit my_profile/email_config.json (gitignored).
  - ALWAYS require explicit user confirmation (--yes gate).
"""

import sys
import os
import re
import glob
import json
import argparse

# Ensure safe console output across all platforms (same convention as other tools)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG = os.path.join(REPO_ROOT, "my_profile", "email_config.json")

# Config keys that could hold secrets — never printed.
SECRET_KEYS = {"imap_password"}


# ---------------------------------------------------------------------------
# Single source of truth: my_profile/email_config.json
# ---------------------------------------------------------------------------

def load_config(config_path):
    """Load sender identity + IMAP connection. Exits with setup hint if missing."""
    path = config_path or DEFAULT_CONFIG
    if not os.path.exists(path):
        print(f"[!] Email config not found: {path}")
        print("    One-time setup: copy my_profile/email_config.example.json")
        print("    to my_profile/email_config.json and fill in your address + app password.")
        print("    See 'One-time setup' in configuration4Draft.md.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # Sane defaults for optional keys
    cfg.setdefault("imap_port", 993)
    cfg.setdefault("imap_folder", "Drafts")
    return cfg


def check_config(cfg):
    """Validate required keys. Returns list of missing key names."""
    required = ["from", "imap_host", "imap_user", "imap_password"]
    return [k for k in required if not cfg.get(k)]


# ---------------------------------------------------------------------------
# Variant A parser (reads outreach_emails.md generated in Step 6)
# ---------------------------------------------------------------------------

def parse_variant_a(outreach_path):
    """Extract (to, subject, body) of Variant A from outreach_emails.md.

    Expected patterns (FR/EN tolerant):
      **Destinataire :** `hr@company.com` / **To:** / **Recipient:**
      **Objet :** ... / **Subject:**
      first ```text fenced block after Variant A header.
    Returns (to, subject, body). Missing recipient -> "" (draft to self).
    """
    with open(outreach_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Isolate Variant A section (up to Variant B header if present)
    m_section = re.search(
        r"(Variant A|Variante A)(.*?)(Variant B|Variante B|Variant C|\Z)",
        text, re.DOTALL | re.IGNORECASE,
    )
    section = m_section.group(2) if m_section else text

    to = ""
    m_to = re.search(
        r"(Destinataire|To|Recipient|Destinataire\s*:|To\s*:)\s*:?.*?`([^`]+@[^`]+)`",
        section, re.IGNORECASE,
    )
    if m_to:
        to = m_to.group(2).strip()
    else:
        # fallback: first email-looking address in backticks in the section
        m_any = re.search(r"`([^`]+@[^`]+)`", section)
        if m_any:
            to = m_any.group(1).strip()

    subject = ""
    m_sub = re.search(
        r"\*\*(Objet|Subject)\s*:?\*\*\s*:?\s*(.+)",
        section, re.IGNORECASE,
    )
    if m_sub:
        subject = m_sub.group(2).strip().strip("`").strip()

    body = ""
    m_body = re.search(r"```text\s*\n(.*?)```", section, re.DOTALL)
    if m_body:
        body = m_body.group(1).strip("\n")
    else:
        # fallback: first fenced block anywhere in section
        m_any_block = re.search(r"```\s*\n(.*?)```", section, re.DOTALL)
        if m_any_block:
            body = m_any_block.group(1).strip("\n")

    return to, subject, body


# ---------------------------------------------------------------------------
# EML builder (stdlib only — always available)
# ---------------------------------------------------------------------------

def build_message(from_addr, to_addr, subject, body_text, attachments):
    from email.message import EmailMessage

    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject or "Job Application"
    msg.set_content(body_text or "")

    for path in attachments or []:
        if not os.path.exists(path):
            print(f"[!] Warning: attachment not found, skipped: {path}")
            continue
        with open(path, "rb") as f:
            data = f.read()
        maintype, subtype = ("application", "pdf") if path.lower().endswith(".pdf") \
            else ("application", "octet-stream")
        msg.add_attachment(
            data, maintype=maintype, subtype=subtype,
            filename=os.path.basename(path),
        )
    return msg


def default_attachments(outreach_path, explicit):
    """Explicit --attach list, or all PDFs in the outreach folder (CV + letter)."""
    if explicit:
        return list(explicit)
    folder = os.path.dirname(os.path.abspath(outreach_path))
    found = sorted(glob.glob(os.path.join(folder, "*.pdf")))
    if found:
        print(f"[*] Auto-attaching {len(found)} PDF(s) from {folder}")
    return found


def provider_eml(msg, outreach_path):
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(outreach_path)), "Draft_Email.eml"
    )
    with open(output_path, "wb") as f:
        f.write(msg.as_bytes())
    print(f"[✓] EML draft saved: {output_path}")
    print("    Double-click to open as draft in Outlook / Apple Mail / Thunderbird,")
    print("    or import into Gmail via Thunderbird. No credentials were needed.")
    return output_path


# ---------------------------------------------------------------------------
# Generic IMAP provider (stdlib imaplib — App Password, works for ALL
# providers: Gmail, Outlook, Yahoo, iCloud, custom domains)
# ---------------------------------------------------------------------------

def provider_imap(msg, cfg):
    import imaplib
    import time

    host = cfg.get("imap_host", "")
    user = cfg.get("imap_user", "")
    password = cfg.get("imap_password", "")
    port = int(cfg.get("imap_port", 993))
    folder = cfg.get("imap_folder", "Drafts") or "Drafts"

    if not host or not user or not password:
        print("[!] Incomplete email config for IMAP (need imap_host, imap_user, imap_password).")
        print("    Fix my_profile/email_config.json — see 'One-time setup' in configuration4Draft.md.")
        return None

    print(f"[*] Connecting to IMAP {host}:{port} as {user} ...")
    mail = imaplib.IMAP4_SSL(host, port)
    mail.login(user, password)
    # Mark as draft: \Draft flag on APPEND
    result, _ = mail.append(
        folder, "\\Draft", imaplib.Time2Internaldate(time.time()),
        msg.as_bytes(),
    )
    mail.logout()
    if result == "OK":
        print(f"[✓] IMAP draft saved in folder '{folder}' on {host}.")
        return True
    print(f"[!] IMAP APPEND failed: {result}")
    return None


# ---------------------------------------------------------------------------
# CLI (minimal: config is the SSOT, content comes from the outreach folder)
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Create a job-application email DRAFT (never auto-send). "
                    "Identity + IMAP come from my_profile/email_config.json; "
                    "recipient/subject/body come from outreach_emails.md."
    )
    parser.add_argument("--provider", choices=["eml", "imap"],
                        default="eml", help="Draft backend: imap (cloud draft for any provider) or eml (local fallback).")
    parser.add_argument("--from-outreach", required=True,
                        help="Path to outreach_emails.md (Variant A is extracted).")
    parser.add_argument("--attach", action="append", default=[],
                        help="PDF to attach (repeatable). Default: all *.pdf in the outreach folder.")
    parser.add_argument("--config", default="",
                        help="Custom config path (default: my_profile/email_config.json).")
    parser.add_argument("--yes", action="store_true",
                        help="Confirm you approved draft creation (anti-spam gate).")
    args = parser.parse_args()

    cfg = load_config(args.config)
    missing = check_config(cfg)
    if missing:
        print(f"[!] email_config.json missing keys: {', '.join(missing)}")
        print("    Fill them in my_profile/email_config.json — see 'One-time setup' in configuration4Draft.md.")
        sys.exit(1)

    if not os.path.exists(args.from_outreach):
        print(f"[!] Outreach file not found: {args.from_outreach}")
        print("    Generate it first (SKILL.md Step 6) before creating a draft.")
        sys.exit(1)

    to_addr, subject, body_text = parse_variant_a(args.from_outreach)
    from_addr = cfg["from"]
    attachments = default_attachments(args.from_outreach, args.attach)

    if not args.yes:
        print("[!] Refusing to create a draft without explicit user confirmation.")
        print("    Re-run with --yes after the user answers YES to:")
        print('    "Found email <to>. Create a mail draft for you? [imap/eml/no]"')
        print(f"    Parsed preview -> To: '{to_addr}' | Subject: '{subject[:80]}' | "
              f"Attachments: {len(attachments)}")
        sys.exit(2)

    if not to_addr:
        print("[!] No recipient in Variant A. Draft will be addressed to yourself —")
        print("    replace the To field when reviewing the draft.")
        to_addr = from_addr
    if not body_text:
        print("[!] Empty body in Variant A. Fix outreach_emails.md first.")
        sys.exit(1)

    # Warn if PDFs are missing (draft without attachments is usually a mistake)
    if not attachments:
        print("[!] Warning: no PDFs found to attach. Draft will have no attachments.")

    msg = build_message(from_addr, to_addr, subject, body_text, attachments)

    if args.provider == "eml":
        provider_eml(msg, args.from_outreach)
    elif args.provider == "imap":
        if not provider_imap(msg, cfg):
            print("[*] IMAP failed — saving .eml fallback instead.")
            provider_eml(msg, args.from_outreach)


if __name__ == "__main__":
    main()
