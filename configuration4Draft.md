# Email Drafts — Setup Guide (do once, ~5 minutes)

After your CV and cover letter are ready, your assistant can place a
ready-to-send email in your mailbox's **Drafts** folder — with the hiring
email address, subject, message, and both PDFs already attached. You only
open the draft, check it, and press Send yourself. Nothing is ever sent
automatically.

---

## What will happen when you apply

At the end of each application, your assistant asks you one question:

> Found email hr@company.com. Create a mail draft for you? [imap/eml/no]

- Answer **`imap`** → the draft appears directly in your mailbox Drafts.
  (Needs the one-time setup below.)
- Answer **`eml`** → you get a file (`Draft_Email.eml`) in the application
  folder. Double-click it and it opens as a draft in Outlook, Apple Mail,
  or Thunderbird. No setup needed.
- Answer **`no`** → nothing happens, the workflow simply ends.

---

## One-time setup (only if you want `imap` drafts)

**Step 1 — Create your email settings file.**

Make a copy of `my_profile/email_config.example.json` and name the copy
`my_profile/email_config.json`. Open it — it looks like this:

```json
{
  "from": "you@gmail.com",
  "imap_host": "imap.gmail.com",
  "imap_port": 993,
  "imap_user": "you@gmail.com",
  "imap_password": "xxxx-xxxx-xxxx-xxxx",
  "imap_folder": "Drafts"
}
```

**Step 2 — Fill in your address.**

Replace `you@gmail.com` (in both `from` and `imap_user`) with your real
email address.

**Step 3 — Copy the server line for your mailbox.**

Find your mailbox below and copy its server address into `imap_host`.
Leave `imap_port` at 993 and `imap_folder` at "Drafts".

| Your mailbox | Write this in `imap_host` |
|---|---|
| Gmail | `imap.gmail.com` |
| Outlook / Hotmail / Microsoft 365 | `outlook.office365.com` |
| Yahoo | `imap.mail.yahoo.com` |
| iCloud | `imap.mail.me.com` |
| Other / company address | Ask your provider for its "IMAP server" |

**Step 4 — Create a special password for the assistant.**

For safety, the assistant never uses your real password. Instead, you
create a separate password just for it (free, takes 1 minute). This is
called an "app password":

- **Gmail:** open your Google Account → Security → turn on 2-Step
  Verification → go back to Security → **App passwords** → create one
  called "Mail" → copy the 16-letter code.
- **Outlook / Hotmail:** open your Microsoft Account → Security → turn
  on 2-step verification → Advanced security options →
  **App passwords → Create** → copy the code.
- **Yahoo:** open your Yahoo Account → Security → generate an
  **app password** → copy it.
- **iCloud:** open appleid.apple.com → Sign-In & Security →
  **App-Specific Passwords** → create one → copy it.

Paste that code into `imap_password`. Done — you will never need to do
this again.

---

## Where is my draft?

- If you answered `imap`: open your mailbox and look in **Drafts**.
  The email is there with the subject, message, and your CV + cover
  letter attached. Read it, fix anything you like, then Send.
- If you answered `eml`: open the application folder and double-click
  `Draft_Email.eml`.

---

## If something doesn't work

- **No draft in my mailbox?** The login details may be wrong. Check that
  the email address and the special password in your settings file have
  no typos. If it still fails, just answer `eml` next time — that always
  works and nothing is lost.
- **"Wrong password" message?** You probably pasted your normal password
  instead of the special app password from Step 4. Create a new app
  password and replace it.
- **Outlook refuses the connection?** Some companies block this kind of
  access — ask your IT team, or simply use `eml`.
- **No hiring email in the job ad?** The draft is addressed to yourself
  so you can add the right recipient when reviewing it.

---

## ⚠️ Please read before continuing — your responsibility

By filling in `imap_password`, you accept the following:

- The app password gives **full access to your mailbox** (read and send),
  not just drafts. That is how email access works — there is no
  "drafts only" option.
- The assistant **will read this password** every time it creates a draft.
  It needs it to log in to your mailbox on your behalf.
- The assistant only creates drafts and **never sends emails on its own**,
  but if someone else obtained your settings file, they could access
  your mailbox with it.

By using this feature, **you take full responsibility** for these risks.
To stay safe:

1. **Never share or publish** `my_profile/email_config.json`. It lives
   only on your computer and is automatically excluded from anything
   shared publicly — keep it that way.
2. **Never paste the password into a chat** with the assistant or anyone
   else. Type it only into the settings file.
3. **Revoke the app password when you're done** (in the same account
   page where you created it). This instantly cuts off access without
   changing your real password. You can create a new one anytime.
4. For extra safety, consider using an **email address dedicated to job
   hunting** rather than your main personal mailbox.

If you are not comfortable with this, simply answer `eml` when asked —
you lose nothing, and no password is ever needed.
