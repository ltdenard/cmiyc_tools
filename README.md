# 🔓 Crack Me If You Can - Utility Scripts

This repository contains a collection of Python scripts designed to assist participants in **Crack Me If You Can (CMIYC)** style password cracking competitions. These tools streamline workflows for:

- 🔐 Decrypting files with known passwords  
- 📧 Submitting cracked hashes via **PGP-encrypted email**  
- 🧹 Sorting and de-duplicating hash lists

---

## 📁 Repository Contents

```
.
├── decrypt_file.py          # Decrypts files using known passwords
├── mail.cfg.example         # Example configuration file for email settings
├── mail_handler.py          # Handles PGP encryption and email submissions
├── send_submission_file.py  # Encrypts and emails submission files
└── sort_dedup.py            # Sorts and removes duplicates from hash lists
```

---

## 🔐 `decrypt_file.py`

Decrypts files using a provided password. Useful for quickly unlocking cracked ZIPs or encrypted archives during competition.

**Usage:**
```bash
python3 decrypt_file.py --input <encrypted_file> --password <password> --output <output_directory>
```

---

## 🧹 `sort_dedup.py`

Sorts a file of cracked hashes and removes duplicates to keep your submission clean.

**Usage:**
```bash
python3 sort_dedup.py --input <hash_list.txt> --output <cleaned_list.txt>
```

---

## 📧 PGP Email Submission Tools

### 🔧 Step 1: Configure Email Settings

Copy the example config and edit:
```bash
cp mail.cfg.example mail.cfg
```

Edit `mail.cfg`:

```ini
[EMAIL]
smtp_server = smtp.example.com
smtp_port = 587
smtp_user = your_email@example.com
smtp_pass = your_password
recipient = recipient@example.com

[PGP]
public_key = path/to/contest_public_key.asc
```

### 📤 Step 2: Send Submission

Use `send_submission_file.py` to encrypt and email your cracked hashes.

**Usage:**
```bash
python3 send_submission_file.py --file <submission_file.txt>
```

Behind the scenes, this uses `mail_handler.py` to PGP-encrypt your file and send it using SMTP.

---

## 🛠️ Requirements

- Python 3.x
- `gnupg` or `python-gnupg` (for PGP encryption)
- `smtplib`, `email`, `configparser` (all standard lib)
- GPG installed and configured
- Required Python packages:

```bash
pip3 install python-gnupg
```

---

## 🚀 Suggested Workflow

```bash
# 1. Decrypt recovered files
python3 decrypt_file.py --input secrets.zip --password cracked123 --output loot/

# 2. Clean up and dedupe hashes
python3 sort_dedup.py --input cracked_hashes.txt --output cleaned_hashes.txt

# 3. Submit via encrypted email
python3 send_submission_file.py --file cleaned_hashes.txt
```

---

## ⚠️ Disclaimer

These scripts are intended for use in **ethical** and **legal** password cracking competitions only, such as DEFCON's Crack Me If You Can (CMIYC). Use responsibly.

---

> “Hash hard, submit smart, and may your wordlists be ever fruitful.” 🔥
