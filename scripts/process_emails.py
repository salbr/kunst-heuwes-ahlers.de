#!/usr/bin/env python3
import imaplib
import email
from email.header import decode_header
import os
import sys
import re
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from html.parser import HTMLParser
import html2text

# Config from environment
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
CLIENT_PASSPHRASE = os.environ.get("CLIENT_PASSPHRASE")
CLIENT_EMAIL = os.environ.get("CLIENT_EMAIL")
IMAP_SERVER = os.environ.get("IMAP_SERVER", "imap.strato.de")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.strato.de")
SMTP_PORT = 465

PROCESSED_FILE = "processed_messages.txt"
BASE_IMAGE_DIR = Path("src/lib/images/kunstwerke")

# Error messages and help texts
ERROR_AUTH_FAILED = """Die Authentifizierung ist fehlgeschlagen.

SO BEHEBST DU DAS PROBLEM:

1. Öffne die E-Mail, die du gerade gesendet hast
2. Klicke auf "Antworten" oder "Weiterleiten"
3. Gehe zur ersten Zeile der E-Mail
4. Die erste Zeile MUSS genau so aussehen: 
   AUTH: DeinPasswort

5. Ersetze "DeinPasswort" durch das Passwort, das du erhalten hast
6. WICHTIG: Nach "AUTH:" muss ein Leerzeichen kommen
7. Das Passwort muss exakt übereinstimmen (Groß-/Kleinschreibung beachten)
8. Sende die E-Mail erneut

BEISPIEL:
AUTH: MeinGeheimesPasswort123
2025-1.jpg
2025-1.ini

Wenn das Problem weiterhin besteht, ruf mich bitte an oder schreib mir bei Signal."""

ERROR_AUTH_FAILED_WITH_ATTACHMENTS = """Die Authentifizierung ist fehlgeschlagen.

SO BEHEBST DU DAS PROBLEM:

1. Öffne die E-Mail, die du gerade gesendet hast
2. Klicke auf "Antworten" oder "Weiterleiten"
3. Gehe zur ersten Zeile der E-Mail
4. Die erste Zeile MUSS genau so aussehen:
   AUTH: DeinPasswort

5. Ersetze "DeinPasswort" durch das Passwort, das du erhalten hast
6. WICHTIG: Nach "AUTH:" muss ein Leerzeichen kommen
7. Das Passwort muss exakt übereinstimmen (Groß-/Kleinschreibung beachten)
8. Hänge deine Bilder wieder an
9. Sende die E-Mail erneut

BEISPIEL:

E-Mail-Text:
AUTH: MeinGeheimesPasswort123

Anhänge:
2025-1.jpg
2025-1.ini

Wenn das Problem weiterhin besteht, ruf mich bitte an oder schreib mir bei Signal."""

ERROR_NO_DELETE_FILENAMES = """Keine Dateinamen zum Löschen gefunden.

SO BEHEBST DU DAS PROBLEM:

1. Öffne eine neue E-Mail
2. Schreibe in den BETREFF: DELETE
3. Schreibe in die E-Mail:

   Erste Zeile: AUTH: DeinPasswort
   Zweite Zeile: Der Name der Datei, die gelöscht werden soll
   Dritte Zeile: (optional) Weitere Dateinamen

BEISPIEL:

Betreff: DELETE

E-Mail-Text:
AUTH: MeinGeheimesPasswort123
2025-5.jpg
2025-5.ini
2024-12.jpg
2024-12.ini

WICHTIG:
- Jeder Dateiname in eine eigene Zeile
- Gib sowohl .jpg als auch .ini Dateien an, wenn beide gelöscht werden sollen
- Der Dateiname muss exakt mit dem Namen auf der Website übereinstimmen"""

HELP_FIX_TYPOS = """SO BEHEBST DU TIPPFEHLER:

1. Überprüfe die Schreibweise der Dateinamen
2. Achte auf:
   - Richtige Jahreszahl am Anfang (z.B. 2025)
   - Bindestrich nach dem Jahr (z.B. 2025-)
   - Richtige Dateiendung (.jpg, .jpeg, .png oder .ini)
3. Schau auf deiner Website nach dem exakten Dateinamen
4. Sende die E-Mail mit dem korrigierten Namen erneut"""

ERROR_NO_FILES = """Keine Dateien gefunden.

SO BEHEBST DU DAS PROBLEM:

1. Öffne eine neue E-Mail mit der Emailadresse, die wir festgelegt haben.
2. Schreibe in die erste Zeile:
   AUTH: DeinPasswort

3. Klicke auf das Büroklammer-Symbol (Anhang hinzufügen)
4. Wähle deine Bilddateien aus:
   - Das Bild selbst (z.B. 2025-1.jpg)
   - Die dazugehörige .ini Datei (z.B. 2025-1.ini)

5. WICHTIG: Die Dateien MÜSSEN so benannt sein:
   - Beginnen mit 4-stelliger Jahreszahl (z.B. 2025)
   - Dann ein Bindestrich (-)
   - Dann eine Nummer oder Name
   - Enden mit .jpg, .jpeg, .png oder .ini

RICHTIGE BEISPIELE:
✓ 2025-1.jpg
✓ 2025-1.ini

FALSCHE BEISPIELE:
✗ bild1.jpg (fehlt Jahr)
✗ 25-1.jpg (Jahr nicht 4-stellig)
✗ 2025_1.jpg (Unterstrich statt Bindestrich)
✗ 2025-1.docx (falscher Dateityp)

6. Sende die E-Mail

Die Website wird innerhalb einer Stunde aktualisiert."""


HELP_REJECTED_FILES = """WARUM WURDEN DATEIEN ABGELEHNT?

Die Dateinamen müssen diesem Format folgen:
JAHR-NAME.ENDUNG

BEISPIELE FÜR RICHTIGE NAMEN:
✓ 2025-1.jpg und 2025-1.ini
✓ 2023-12.png und 2023-12.ini

SO BENENNST DU DATEIEN UM:

Windows:
1. Öffne den Ordner mit deinen Bildern
2. Rechtsklick auf die Datei
3. Wähle "Umbenennen"
4. Gib den neuen Namen ein (z.B. 2025-1.jpg)
5. Drücke Enter

WICHTIG:
- Das Jahr muss 4-stellig sein (2025, nicht 25)
- Nach dem Jahr MUSS ein Bindestrich - kommen
- Erlaubte Endungen: .jpg, .jpeg, .png, .ini
- Zu jedem Bild gehört eine .ini Datei mit gleichem Namen

Nachdem du die Dateien umbenannt hast, sende die E-Mail erneut."""


def decode_quoted_printable(text):
    # Remove soft line breaks (= followed by newline)
    text = re.sub(r"=\s*\n", "", text)

    # Decode =XX patterns to bytes then UTF-8
    def replace_hex(match):
        return bytes([int(match.group(1), 16)])

    # Convert string to bytes, replace patterns, decode UTF-8
    text_bytes = text.encode("latin1")
    text_bytes = re.sub(rb"=([0-9A-F]{2})", replace_hex, text_bytes)
    return text_bytes.decode("utf-8")


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.text.append("\n")

    def handle_entityref(self, name):
        if name == "nbsp":
            self.text.append(" ")

    def get_text(self):
        return "".join(self.text)


def load_processed_ids():
    if not Path(PROCESSED_FILE).exists():
        return set()
    with open(PROCESSED_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save_processed_id(msg_id):
    with open(PROCESSED_FILE, "a") as f:
        f.write(f"{msg_id}\n")


def send_reply(to_addr, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send reply to {to_addr}: {e}")


def extract_year_from_filename(filename):
    match = re.match(r"^(\d{4})-", filename)
    return match.group(1) if match else None


def validate_auth(msg):
    body = ""

    # Extract all text/html parts
    for part in msg.walk():
        content_type = part.get_content_type()

        if content_type not in ["text/plain", "text/html"]:
            continue

        content = part.get_payload(decode=True)

        if not content:
            continue
        body = content.decode("utf-8", errors="ignore")

        if content_type == "text/html":
            body = html2text.html2text(body)
    # Check passphrase
    if CLIENT_PASSPHRASE not in body:
        print("Auth failed: passphrase not found")
        return False, body

    return True, body


def process_delete(msg, sender):
    subject = msg["Subject"]
    auth_valid, body = validate_auth(msg)

    if not auth_valid:
        send_reply(
            sender, "FEHLER: Authentifizierung fehlgeschlagen", ERROR_AUTH_FAILED
        )
        return

    lines = body.split("\n")[1:]  # Skip AUTH line
    filenames = [
        line.strip().lower().replace(" ", "") for line in lines if line.strip()
    ]

    if not filenames:
        send_reply(
            sender, "FEHLER: Keine Dateinamen angegeben", ERROR_NO_DELETE_FILENAMES
        )
        return

    deleted = []
    not_found = []

    for filename in filenames:
        year = extract_year_from_filename(filename)
        if not year:
            not_found.append(f"{filename} (kein Jahr erkennbar)")
            continue

        year_dir = BASE_IMAGE_DIR / year
        file_path = year_dir / filename

        if file_path.exists():
            file_path.unlink()
            deleted.append(filename)
        else:
            not_found.append(filename)

    response = "Löschvorgang abgeschlossen:\n\n"
    if deleted:
        response += (
            "✓ ERFOLGREICH GELÖSCHT:\n"
            + "\n".join(f"  - {f}" for f in deleted)
            + "\n\n"
        )
    if not_found:
        response += (
            "✗ NICHT GEFUNDEN (möglicherweise Tippfehler):\n"
            + "\n".join(f"  - {f}" for f in not_found)
            + "\n\n"
        )
        response += HELP_FIX_TYPOS

    send_reply(sender, "Löschvorgang abgeschlossen", response)


def process_add_edit(msg, sender):
    auth_valid, body = validate_auth(msg)

    if not auth_valid:
        send_reply(
            sender,
            "FEHLER: Authentifizierung fehlgeschlagen",
            ERROR_AUTH_FAILED_WITH_ATTACHMENTS,
        )
        return

    added = []
    edited = []
    rejected = []

    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue

        filename = part.get_filename()
        if not filename:
            continue

        # Decode filename if encoded
        if decode_header(filename)[0][1]:
            filename = decode_header(filename)[0][0].decode(
                decode_header(filename)[0][1]
            )
        filename = filename.lower()

        # Validate filename format
        year = extract_year_from_filename(filename)
        if not year:
            rejected.append(f"{filename} (kein Jahr im Format YYYY-*.jpg/ini)")
            continue

        # Only accept .jpg, .jpeg, .png, .ini
        ext = Path(filename).suffix
        if ext not in [".jpg", ".jpeg", ".png", ".ini"]:
            rejected.append(f"{filename} (ungültiger Dateityp)")
            continue

        year_dir = BASE_IMAGE_DIR / year
        year_dir.mkdir(parents=True, exist_ok=True)

        file_path = year_dir / filename
        existed = file_path.exists()

        with open(file_path, "wb") as f:
            f.write(part.get_payload(decode=True))

        if existed:
            edited.append(filename)
        else:
            added.append(filename)

    if not added and not edited and not rejected:
        send_reply(sender, "FEHLER: Keine Dateien gefunden", ERROR_NO_FILES)
        return

    response = "Upload abgeschlossen:\n\n"

    if added:
        response += (
            "✓ NEU HINZUGEFÜGT:\n" + "\n".join(f"  - {f}" for f in added) + "\n\n"
        )

    if edited:
        response += "✓ AKTUALISIERT:\n" + "\n".join(f"  - {f}" for f in edited) + "\n\n"

    if rejected:
        response += "✗ ABGELEHNT:\n" + "\n".join(f"  - {f}" for f in rejected) + "\n\n"
        response += HELP_REJECTED_FILES

    if added or edited:
        response += (
            "\nDie Website wird innerhalb einer Stunde automatisch aktualisiert."
        )

    send_reply(sender, "Upload abgeschlossen", response)


def main():
    if not all([EMAIL_USER, EMAIL_PASS, CLIENT_PASSPHRASE, CLIENT_EMAIL]):
        print("Missing required environment variables")
        sys.exit(1)

    processed_ids = load_processed_ids()

    # Connect to IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    # Search for all emails
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        msg_id = msg["Message-ID"]
        sender = email.utils.parseaddr(msg["From"])[1]

        # Delete emails from unauthorized senders
        if sender.lower() != CLIENT_EMAIL.lower():
            mail.store(email_id, "+FLAGS", "\\Deleted")
            print(f"Deleted email from unauthorized sender: {sender}")
            continue

        # Skip already processed client emails
        if msg_id in processed_ids:
            continue

        subject = msg["Subject"] or ""
        if decode_header(subject)[0][1]:
            subject = decode_header(subject)[0][0].decode(decode_header(subject)[0][1])

        print(f"Processing email from {sender}: {subject}")

        if "DELETE" in subject.upper():
            process_delete(msg, sender)
        else:
            process_add_edit(msg, sender)

        save_processed_id(msg_id)

    # Expunge deleted messages
    mail.expunge()
    mail.close()
    mail.logout()


if __name__ == "__main__":
    main()
