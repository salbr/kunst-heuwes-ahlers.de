#!/usr/bin/env python3
"""
Comprehensive test suite for process_emails.py

Run with: python3 test_process_emails.py -v
"""
import unittest
from unittest.mock import patch, MagicMock, call
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import Path
import os
import sys
import tempfile
import shutil

# Import the module to test
sys.path.insert(0, os.path.dirname(__file__))
import process_emails


class TestEmailProcessing(unittest.TestCase):
    """Tests for email processing functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()

        # Set up environment variables
        os.environ["EMAIL_USER"] = "test@example.net"
        os.environ["EMAIL_PASS"] = "testpass"
        os.environ["CLIENT_PASSPHRASE"] = "aaaaaaaa-ggggg-77777"
        os.environ["CLIENT_EMAIL"] = "client@example.net"
        os.environ["IMAP_SERVER"] = "imap.strato.de"
        os.environ["SMTP_SERVER"] = "smtp.strato.de"

        # Reload module to pick up env vars
        import importlib

        importlib.reload(process_emails)

        # Create test directories
        self.base_image_dir = Path(self.test_dir) / "static/images/kunstwerke"
        self.base_image_dir.mkdir(parents=True, exist_ok=True)

        # Override paths in module
        process_emails.BASE_IMAGE_DIR = self.base_image_dir
        process_emails.PROCESSED_FILE = os.path.join(
            self.test_dir, "processed_messages.txt"
        )

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_test_email(
        self,
        subject="Test",
        body="AUTH: aaaaaaaa-ggggg-77777",
        from_addr="client@example.net",
        attachments=None,
    ):
        """Create a test email message"""
        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = "test@example.net"
        msg["Subject"] = subject
        msg["Message-ID"] = f"<{hash(body)}@example.net>"

        msg.attach(MIMEText(body, "plain"))

        if attachments:
            for filename, content in attachments.items():
                if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    part = MIMEImage(content, _subtype="jpeg")
                    part.add_header(
                        "Content-Disposition", f"attachment; filename={filename}"
                    )
                elif filename.endswith(".png"):
                    part = MIMEImage(content, _subtype="png")
                    part.add_header(
                        "Content-Disposition", f"attachment; filename={filename}"
                    )
                else:
                    part = MIMEText(
                        content.decode() if isinstance(content, bytes) else content
                    )
                    part.add_header(
                        "Content-Disposition", f"attachment; filename={filename}"
                    )
                msg.attach(part)

        return email.message_from_bytes(msg.as_bytes())

    # ===== Utility Function Tests =====
    def test_decode_quoted_printable(self):
        """Test quoted-printable decoding"""
        test_cases = [
            ("AUTH=2E test", "AUTH. test"),
            ("This is a long=\nline", "This is a longline"),
            ("Diplom-Sozialp=C3=A4dagogin", "Diplom-Sozialpädagogin"),
            ("Test=20space", "Test space"),
            # Soft line break: = at end of line is removed along with the newline
            ("AUTH=2E aaaaaaaa-ggggg-77=\n777", "AUTH. aaaaaaaa-ggggg-77777"),
            # Note: whitespace AFTER the newline is preserved (RFC 2045 compliant)
            # In real emails, HTML parsers may collapse whitespace during extraction
        ]

        for input_text, expected in test_cases:
            result = process_emails.decode_quoted_printable(input_text)
            self.assertEqual(result, expected, f"Failed for: {input_text}")

    def test_text_extractor(self):
        """Test HTML text extraction"""
        html = """
        <html>
            <body>
                <div>AUTH: testpass</div>
                <br>
                <div>2025-1.jpg</div>
                <div>Test&nbsp;content</div>
            </body>
        </html>
        """
        extractor = process_emails.TextExtractor()
        extractor.feed(html)
        text = extractor.get_text()

        self.assertIn("AUTH: testpass", text)
        self.assertIn("2025-1.jpg", text)
        # nbsp is converted to space
        self.assertIn("Test content", text.replace("\xa0", " "))

    def test_extract_year_from_filename(self):
        """Test year extraction from filenames"""
        test_cases = [
            ("2025-1.jpg", "2025"),
            ("2023-test.ini", "2023"),
            ("2024-abc.png", "2024"),
            ("test.jpg", None),
            ("25-1.jpg", None),
            ("202-test.jpg", None),
        ]

        for filename, expected in test_cases:
            result = process_emails.extract_year_from_filename(filename)
            self.assertEqual(result, expected, f"Failed for: {filename}")

    def test_load_save_processed_ids(self):
        """Test loading and saving processed message IDs"""
        # Test empty file
        ids = process_emails.load_processed_ids()
        self.assertEqual(ids, set())

        # Save some IDs
        process_emails.save_processed_id("msg1")
        process_emails.save_processed_id("msg2")
        process_emails.save_processed_id("msg3")

        # Load them back
        ids = process_emails.load_processed_ids()
        self.assertEqual(ids, {"msg1", "msg2", "msg3"})

        # Test duplicate handling
        process_emails.save_processed_id("msg1")
        ids = process_emails.load_processed_ids()
        self.assertEqual(len(ids), 3)  # Should still be 3

    # ===== Authentication Tests =====

    def test_validate_auth_success(self):
        """Test successful authentication with correct passphrase"""
        msg = self.create_test_email(body="AUTH: aaaaaaaa-ggggg-77777\nSome content")
        is_valid, body = process_emails.validate_auth(msg)

        self.assertTrue(is_valid)
        self.assertIn("aaaaaaaa-ggggg-77777", body)

    def test_validate_auth_failure_wrong_passphrase(self):
        """Test failed authentication with wrong passphrase"""
        msg = self.create_test_email(body="AUTH: wrong-password")
        is_valid, body = process_emails.validate_auth(msg)

        self.assertFalse(is_valid)

    def test_validate_auth_failure_no_passphrase(self):
        """Test failed authentication with no passphrase"""
        msg = self.create_test_email(body="Just some content without auth")
        is_valid, body = process_emails.validate_auth(msg)

        self.assertFalse(is_valid)

    def test_validate_auth_html_content(self):
        """Test authentication with HTML body"""
        msg = MIMEMultipart()
        msg["From"] = "client@example.net"
        msg["Subject"] = "Test"
        msg["Message-ID"] = "<html-test@example.net>"

        html_body = """
        <html>
            <body>
                <div>AUTH: aaaaaaaa-ggggg-77777</div>
                <div>2025-1.jpg</div>
            </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        parsed_msg = email.message_from_bytes(msg.as_bytes())
        is_valid, body = process_emails.validate_auth(parsed_msg)

        self.assertTrue(is_valid)

    # ===== Delete Operation Tests =====

    @patch("process_emails.send_reply")
    def test_process_delete_success(self, mock_send):
        """Test successful file deletion"""
        # Create files to delete
        year_dir = self.base_image_dir / "2025"
        year_dir.mkdir(parents=True, exist_ok=True)

        test_jpg = year_dir / "2025-1.jpg"
        test_ini = year_dir / "2025-1.ini"
        test_jpg.write_bytes(b"test image")
        test_ini.write_text("test ini")

        # Create delete email
        msg = self.create_test_email(
            subject="DELETE", body="AUTH: aaaaaaaa-ggggg-77777\n2025-1.jpg\n2025-1.ini"
        )

        process_emails.process_delete(msg, "client@example.net")

        # Verify files were deleted
        self.assertFalse(test_jpg.exists())
        self.assertFalse(test_ini.exists())

        # Verify reply
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        self.assertIn("ERFOLGREICH GELÖSCHT", args[2])
        self.assertIn("2025-1.jpg", args[2])

    @patch("process_emails.send_reply")
    def test_process_delete_file_not_found(self, mock_send):
        """Test deletion of non-existent files"""
        msg = self.create_test_email(
            subject="DELETE",
            body="AUTH: aaaaaaaa-ggggg-77777\n2025-99.jpg\n2025-99.ini",
        )

        process_emails.process_delete(msg, "client@example.net")

        # Verify error reply
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        self.assertIn("NICHT GEFUNDEN", args[2])

    @patch("process_emails.send_reply")
    def test_process_delete_mixed_results(self, mock_send):
        """Test deletion with mix of existing and non-existing files"""
        # Create one file
        year_dir = self.base_image_dir / "2025"
        year_dir.mkdir(parents=True, exist_ok=True)
        (year_dir / "2025-1.jpg").write_bytes(b"test")

        msg = self.create_test_email(
            subject="DELETE", body="AUTH: aaaaaaaa-ggggg-77777\n2025-1.jpg\n2025-99.jpg"
        )

        process_emails.process_delete(msg, "client@example.net")

        args = mock_send.call_args[0]
        self.assertIn("ERFOLGREICH GELÖSCHT", args[2])
        self.assertIn("2025-1.jpg", args[2])
        self.assertIn("NICHT GEFUNDEN", args[2])
        self.assertIn("2025-99.jpg", args[2])

    @patch("process_emails.send_reply")
    def test_process_delete_auth_failure(self, mock_send):
        """Test delete with failed authentication"""
        msg = self.create_test_email(
            subject="DELETE", body="AUTH: wrong-password\n2025-1.jpg"
        )

        process_emails.process_delete(msg, "client@example.net")

        # Verify error reply
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        self.assertIn("Authentifizierung fehlgeschlagen", args[1])

    @patch("process_emails.send_reply")
    def test_process_delete_no_filenames(self, mock_send):
        """Test delete with no filenames provided"""
        msg = self.create_test_email(
            subject="DELETE", body="AUTH: aaaaaaaa-ggggg-77777\n"
        )

        process_emails.process_delete(msg, "client@example.net")

        # Verify error reply
        args = mock_send.call_args[0]
        self.assertIn("Keine Dateinamen", args[1])

    # ===== Add/Edit Operation Tests =====

    @patch("process_emails.send_reply")
    def test_process_add_edit_new_file(self, mock_send):
        """Test adding a new file"""
        msg = self.create_test_email(
            body="AUTH: aaaaaaaa-ggggg-77777",
            attachments={
                "2025-1.jpg": b"fake image data",
                "2025-1.ini": b"fake ini data",
            },
        )

        process_emails.process_add_edit(msg, "client@example.net")

        # Verify files were created
        year_dir = self.base_image_dir / "2025"
        self.assertTrue((year_dir / "2025-1.jpg").exists())
        self.assertTrue((year_dir / "2025-1.ini").exists())
        self.assertEqual((year_dir / "2025-1.jpg").read_bytes(), b"fake image data")

        # Verify reply
        args = mock_send.call_args[0]
        self.assertIn("NEU HINZUGEFÜGT", args[2])

    @patch("process_emails.send_reply")
    def test_process_add_edit_update_existing(self, mock_send):
        """Test updating existing files"""
        # Create existing file
        year_dir = self.base_image_dir / "2025"
        year_dir.mkdir(parents=True, exist_ok=True)
        (year_dir / "2025-1.jpg").write_bytes(b"original content")

        msg = self.create_test_email(
            body="AUTH: aaaaaaaa-ggggg-77777",
            attachments={"2025-1.jpg": b"updated content"},
        )

        process_emails.process_add_edit(msg, "client@example.net")

        # Verify file was updated
        self.assertEqual((year_dir / "2025-1.jpg").read_bytes(), b"updated content")

        # Verify reply
        args = mock_send.call_args[0]
        self.assertIn("AKTUALISIERT", args[2])

    @patch("process_emails.send_reply")
    def test_process_add_edit_invalid_filename(self, mock_send):
        """Test rejection of invalid filenames"""
        msg = self.create_test_email(
            body="AUTH: aaaaaaaa-ggggg-77777",
            attachments={
                "invalid.jpg": b"data",
                "25-1.jpg": b"data",
                "2025_1.jpg": b"data",
            },
        )

        process_emails.process_add_edit(msg, "client@example.net")

        # Verify rejection
        args = mock_send.call_args[0]
        self.assertIn("ABGELEHNT", args[2])
        self.assertIn("invalid.jpg", args[2])

    @patch("process_emails.send_reply")
    def test_process_add_edit_invalid_extension(self, mock_send):
        """Test rejection of invalid file extensions"""
        msg = self.create_test_email(
            body="AUTH: aaaaaaaa-ggggg-77777",
            attachments={
                "2025-1.txt": b"data",
                "2025-1.docx": b"data",
                "2025-1.exe": b"data",
            },
        )

        process_emails.process_add_edit(msg, "client@example.net")

        # Verify rejection
        args = mock_send.call_args[0]
        self.assertIn("ABGELEHNT", args[2])

    @patch("process_emails.send_reply")
    def test_process_add_edit_no_attachments(self, mock_send):
        """Test with no attachments"""
        msg = self.create_test_email(body="AUTH: aaaaaaaa-ggggg-77777")

        process_emails.process_add_edit(msg, "client@example.net")

        # Verify error reply
        args = mock_send.call_args[0]
        self.assertIn("Keine Dateien gefunden", args[1])

    @patch("process_emails.send_reply")
    def test_process_add_edit_auth_failure(self, mock_send):
        """Test add/edit with failed authentication"""
        msg = self.create_test_email(
            body="AUTH: wrong-password", attachments={"2025-1.jpg": b"data"}
        )

        process_emails.process_add_edit(msg, "client@example.net")

        # Verify error reply
        args = mock_send.call_args[0]
        self.assertIn("Authentifizierung fehlgeschlagen", args[1])

    @patch("process_emails.send_reply")
    def test_process_add_edit_mixed_valid_invalid(self, mock_send):
        """Test with mix of valid and invalid files"""
        msg = self.create_test_email(
            body="AUTH: aaaaaaaa-ggggg-77777",
            attachments={
                "2025-1.jpg": b"valid",
                "2025-2.png": b"valid",
                "invalid.jpg": b"invalid",
                "2025-3.txt": b"invalid",
            },
        )

        process_emails.process_add_edit(msg, "client@example.net")

        # Verify valid files were added
        year_dir = self.base_image_dir / "2025"
        self.assertTrue((year_dir / "2025-1.jpg").exists())
        self.assertTrue((year_dir / "2025-2.png").exists())

        # Verify reply shows both success and rejection
        args = mock_send.call_args[0]
        self.assertIn("NEU HINZUGEFÜGT", args[2])
        self.assertIn("ABGELEHNT", args[2])

    # ===== SMTP Reply Tests =====

    @patch("smtplib.SMTP_SSL")
    def test_send_reply_success(self, mock_smtp):
        """Test sending email replies"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        process_emails.send_reply("client@example.net", "Test Subject", "Test Body")

        # Verify SMTP operations
        mock_smtp.assert_called_once_with("smtp.strato.de", 465)
        mock_server.login.assert_called_once_with("test@example.net", "testpass")
        mock_server.send_message.assert_called_once()

        # Verify message content
        msg = mock_server.send_message.call_args[0][0]
        self.assertEqual(msg["From"], "test@example.net")
        self.assertEqual(msg["To"], "client@example.net")
        self.assertEqual(msg["Subject"], "Test Subject")

    @patch("smtplib.SMTP_SSL")
    def test_send_reply_failure(self, mock_smtp):
        """Test send_reply handles SMTP errors gracefully"""
        mock_smtp.side_effect = Exception("SMTP error")

        # Should not raise exception
        process_emails.send_reply("client@example.net", "Subject", "Body")

    # ===== Main Function Tests =====

    @patch("imaplib.IMAP4_SSL")
    @patch("process_emails.send_reply")
    def test_main_process_delete(self, mock_send, mock_imap):
        """Test main function processes DELETE emails"""
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail

        # Create files to delete
        year_dir = self.base_image_dir / "2025"
        year_dir.mkdir(parents=True, exist_ok=True)
        (year_dir / "2025-1.jpg").write_bytes(b"test")

        # Create DELETE email
        test_msg = self.create_test_email(
            subject="DELETE", body="AUTH: aaaaaaaa-ggggg-77777\n2025-1.jpg"
        )

        mock_mail.search.return_value = ("OK", [b"1"])
        mock_mail.fetch.return_value = ("OK", [(None, test_msg.as_bytes())])

        process_emails.main()

        # Verify file was deleted
        self.assertFalse((year_dir / "2025-1.jpg").exists())

    @patch("imaplib.IMAP4_SSL")
    @patch("process_emails.send_reply")
    def test_main_process_add(self, mock_send, mock_imap):
        """Test main function processes ADD emails"""
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail

        test_msg = self.create_test_email(
            body="AUTH: aaaaaaaa-ggggg-77777", attachments={"2025-1.jpg": b"test image"}
        )

        mock_mail.search.return_value = ("OK", [b"1"])
        mock_mail.fetch.return_value = ("OK", [(None, test_msg.as_bytes())])

        process_emails.main()

        # Verify file was created
        year_dir = self.base_image_dir / "2025"
        self.assertTrue((year_dir / "2025-1.jpg").exists())

    @patch("imaplib.IMAP4_SSL")
    def test_main_unauthorized_sender(self, mock_imap):
        """Test main function deletes emails from unauthorized senders"""
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail

        test_msg = self.create_test_email(from_addr="unauthorized@example.com")

        mock_mail.search.return_value = ("OK", [b"1"])
        mock_mail.fetch.return_value = ("OK", [(None, test_msg.as_bytes())])

        process_emails.main()

        # Verify email was marked for deletion
        mock_mail.store.assert_called_with(b"1", "+FLAGS", "\\Deleted")

    @patch("imaplib.IMAP4_SSL")
    def test_main_skip_processed(self, mock_imap):
        """Test main function skips already processed emails"""
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail

        test_msg = self.create_test_email(body="AUTH: aaaaaaaa-ggggg-77777")
        msg_id = test_msg["Message-ID"]

        # Mark as already processed
        process_emails.save_processed_id(msg_id)

        mock_mail.search.return_value = ("OK", [b"1"])
        mock_mail.fetch.return_value = ("OK", [(None, test_msg.as_bytes())])

        process_emails.main()

        # Verify no processing occurred (no new files created)
        self.assertEqual(len(list(self.base_image_dir.rglob("*.*"))), 0)

    def test_main_missing_env_vars(self):
        """Test main function exits when environment variables are missing"""
        # Save and remove required env var
        saved_user = os.environ.get("EMAIL_USER")
        if "EMAIL_USER" in os.environ:
            del os.environ["EMAIL_USER"]

        # Reload to pick up missing env var
        import importlib

        importlib.reload(process_emails)

        with self.assertRaises(SystemExit):
            process_emails.main()

        # Restore
        if saved_user:
            os.environ["EMAIL_USER"] = saved_user
        importlib.reload(process_emails)


class TestFileValidation(unittest.TestCase):
    """Tests for file validation logic"""

    def test_valid_filenames(self):
        """Test that valid filenames are accepted"""
        valid_names = [
            "2025-1.jpg",
            "2023-test.png",
            "2024-123.jpeg",
            "2025-config.ini",
            "2020-001.jpg",
            "2099-xyz.png",
        ]

        for name in valid_names:
            year = process_emails.extract_year_from_filename(name)
            self.assertIsNotNone(year, f"Failed for {name}")
            self.assertEqual(len(year), 4)

    def test_invalid_filenames(self):
        """Test that invalid filenames are rejected"""
        invalid_names = [
            ("test.jpg", "no year prefix"),
            ("25-1.jpg", "year too short"),
            ("202-1.jpg", "year too short"),
            ("20255-1.jpg", "year too long"),
            ("abcd-1.jpg", "non-numeric year"),
        ]

        for name, reason in invalid_names:
            year = process_emails.extract_year_from_filename(name)
            self.assertIsNone(year, f"Should have failed for {name} ({reason})")

    def test_filename_edge_cases(self):
        """Test edge cases in filename validation"""
        test_cases = [
            ("2025-.jpg", "2025"),  # Empty name part
            ("2025-a.jpg", "2025"),  # Single char name
            ("2025-very-long-name-with-many-dashes.jpg", "2025"),  # Multiple dashes
        ]

        for name, expected_year in test_cases:
            year = process_emails.extract_year_from_filename(name)
            self.assertEqual(year, expected_year, f"Failed for {name}")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
